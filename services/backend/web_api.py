from fastapi import FastAPI, Query
from typing import List, Dict

from models import Show, Episode, Content
from data_processing.database import Database
from data_processing.queries import *
from data_processing.youtube_api import YoutubeAPI
from data_processing.shows_api import ShowsAPI


app = FastAPI()
db = Database()
youtube_api = YoutubeAPI()
shows_api = ShowsAPI()


@app.get("/search_suggestions")
async def get_search_suggestions(query: str = Query(..., min_length=1)):
    suggestions = await db.get_suggestions(query, index='shows', field='title')
    return suggestions


@app.get("/show_data")
def get_show_data(title: str):
    show_query = get_show_by_title_query(title)
    show_response = db.read(index="shows", query=show_query)
    show_hits = show_response["hits"]["hits"]

    # if we have no info on the show or if we have only title,
    # we will get the data from the API
    if not show_hits or not show_hits[0]["_source"]["internal_id"]:
        show_data = shows_api.search(title)
    else:
        show_data = show_hits[0]["_source"]

        # if we have FULL info about the show, the internal_id will be present
        if show_data["internal_id"]:
            episode_query = get_episodes_by_show_id_query(show_data["internal_id"])
            episode_response = db.read(index="episodes", query=episode_query)
            episode_hits = episode_response["hits"]["hits"]
            episodes = [Episode(**episode["_source"]) for episode in episode_hits]
            show_data["episodes"] = episodes

    return show_data


@app.get("/search_content", response_model=List[Content])
def search_content(query: str = Query(..., min_length=1), episode_range: str = Query(..., regex="^\\d+-\\d+$")):
    start_date, end_date = get_start_and_end_dates(episode_range)
    query = get_content_query(query, start_date, end_date)
    response = db.read(index="content", query=query)
    hits = response["hits"]["hits"]

    if hits:
        content_results = [Content(**hit["_source"]) for hit in hits]
    else:
        content_results = youtube_api.search(query)

    return content_results


def get_start_and_end_dates(episode_range: str):
    start_episode, end_episode = map(int, episode_range.split("-"))
    start_episode_data = get_air_date_of_episode_query(start_episode)
    start_date = db.read(index="episodes", query=start_episode_data)["hits"]["hits"][0]["_source"]["air_date"]
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_episode_data = get_air_date_of_episode_query(end_episode)
    end_date = db.read(index="episodes", query=end_episode_data)["hits"]["hits"][0]["_source"]["air_date"]
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    return start_date, end_date
