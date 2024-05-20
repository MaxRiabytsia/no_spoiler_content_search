from fastapi import FastAPI, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict

from models import Show, Episode, Content
from database import Database
from data_processing.queries import *
from youtube_api import YoutubeAPI
from shows_api import ShowsAPI
from dotenv import load_dotenv


load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = Database()
youtube_api = YoutubeAPI()
shows_api = ShowsAPI()


@app.get("/search_suggestions")
async def get_search_suggestions(query: str = Query(..., min_length=1)):
    suggestions = await db.get_suggestions(query, index='show', field='title')
    suggestions = [Show(**suggestion["_source"]) for suggestion in suggestions]
    return suggestions


@app.get("/show_data")
def get_show_data(title: str, background_tasks: BackgroundTasks):
    show_query = get_show_by_title_query(title)
    show_response = db.read(index="show", query=show_query)
    show_hits = show_response["hits"]["hits"]

    # if we have no info on the show or if we have only title,
    # we will get the data from the API
    if not show_hits or not show_hits[0]["_source"]["external_id"]:
        print(f"Show not found in ES, searching for {title} in API")
        show, episodes = shows_api.search(title)
        if show:
            background_tasks.add_task(db.delete, show_title=title)
            background_tasks.add_task(db.write, data=[show])
            background_tasks.add_task(db.write, data=episodes)
    else:
        print("Show found in ES")
        show_data = show_hits[0]["_source"]
        show = Show(**show_data)
        episode_query = get_episodes_by_show_id_query(show_data["external_id"])
        episode_response = db.read(index="episode", query=episode_query)
        episode_hits = episode_response["hits"]["hits"]
        episodes = [Episode(**episode["_source"]) for episode in episode_hits]

    return show, episodes


@app.get("/search_content", response_model=List[Content])
def search_content(query: str = Query(..., min_length=1),
                   episode_range: str = Query(..., regex="^\\d+-\\d+$")):
    start_episode_id, end_episode_id = map(int, episode_range.split("-"))
    start_date, end_date = get_start_and_end_dates(start_episode_id, end_episode_id)

    content_results = youtube_api.search_videos(query, start_date, end_date, end_episode_id)

    return content_results


def get_start_and_end_dates(start_episode_id: int, end_episode_id: int) -> tuple[datetime, datetime]:
    def get_correct_date_format(date: str) -> datetime:
        return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")

    start_episode_data = get_episode_data_query(start_episode_id)
    start_date = db.read(index="episode", query=start_episode_data)["hits"]["hits"][0]["_source"]["air_date"]
    start_date = get_correct_date_format(start_date)
    end_episode_data = get_episode_data_query(end_episode_id)
    end_date = db.read(index="episode", query=end_episode_data)["hits"]["hits"][0]["_source"]["air_date"]
    end_date = get_correct_date_format(end_date)

    return start_date, end_date
