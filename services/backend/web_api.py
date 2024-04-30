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
    return suggestions


@app.get("/show_data")
def get_show_data(title: str, background_tasks: BackgroundTasks):
    show_query = get_show_by_title_query(title)
    show_response = db.read(index="show", query=show_query)
    show_hits = show_response["hits"]["hits"]

    # if we have no info on the show or if we have only title,
    # we will get the data from the API
    if not show_hits or not show_hits[0]["_source"]["external_id"]:
        show, episodes = shows_api.search(title)
        if show:
            background_tasks.add_task(db.write, data=[show])
            background_tasks.add_task(db.write, data=episodes)
    else:
        show_data = show_hits[0]["_source"]
        show = Show(**show_data)
        episode_query = get_episodes_by_show_id_query(show_data["external_id"])
        episode_response = db.read(index="episode", query=episode_query)
        episode_hits = episode_response["hits"]["hits"]
        episodes = [Episode(**episode["_source"]) for episode in episode_hits]

    return show, episodes


@app.get("/search_content", response_model=List[Content])
def search_content(background_tasks: BackgroundTasks, query: str = Query(..., min_length=1),
                   episode_range: str = Query(..., regex="^\\d+-\\d+$")):
    start_episode_id, end_episode_id = map(int, episode_range.split("-"))
    start_date, end_date = get_start_and_end_dates(start_episode_id, end_episode_id)
    es_query = get_content_query(query, start_date, end_date)
    response = db.read(index="content", query=es_query)
    hits = response["hits"]["hits"]

    if hits:
        content_results = [Content(**hit["_source"]) for hit in hits]
    else:
        content_results = youtube_api.search_videos(query, start_date, end_date, end_episode_id)
        if content_results:
            background_tasks.add_task(db.write, data=content_results)

    return content_results


def get_start_and_end_dates(start_episode_id: int, end_episode_id: int) -> tuple[datetime, datetime]:
    start_episode_data = get_episode_data_query(start_episode_id)
    start_date = db.read(index="episodes", query=start_episode_data)["hits"]["hits"][0]["_source"]["air_date"]
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_episode_data = get_episode_data_query(end_episode_id)
    end_date = db.read(index="episodes", query=end_episode_data)["hits"]["hits"][0]["_source"]["air_date"]
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    return start_date, end_date
