from fastapi import FastAPI
from models import Show, Episode, Content
from typing import List
from datetime import datetime


app = FastAPI()


@app.get("/shows", response_model=List[Show])
def get_shows():
    shows = [
        Show(id=1, internal_id="show1", title="Show 1", description="Description 1", rating=4.5,
             poster_url="poster1.jpg", is_airing=True, created_at=datetime.now(), updated_at=datetime.now()),
        Show(id=2, internal_id="show2", title="Show 2", description="Description 2", rating=4.2,
             poster_url="poster2.jpg", is_airing=False, created_at=datetime.now(), updated_at=datetime.now())
    ]
    return shows


@app.get("/episodes", response_model=List[Episode])
def get_episodes():
    episodes = [
        Episode(id=1, internal_id="episode1", name="Episode 1", show_id=1, season=1, number=1,
                is_last_of_the_season=False, is_last_of_the_show=False, description="Description 1",
                air_date=datetime.now(), next_episode_air_date=datetime.now(), created_at=datetime.now(),
                updated_at=datetime.now()),
        Episode(id=2, internal_id="episode2", name="Episode 2", show_id=1, season=1, number=2,
                is_last_of_the_season=True, is_last_of_the_show=False, description="Description 2",
                air_date=datetime.now(), next_episode_air_date=datetime.now(), created_at=datetime.now(),
                updated_at=datetime.now())
    ]
    return episodes


@app.get("/contents", response_model=List[Content])
def get_contents():
    contents = [
        Content(id=1, internal_id="content1", episode_id=1, title="Content 1", url="url1", content_type="video",
                view_count=100, like_count=10, published_date=datetime.now(), created_at=datetime.now(),
                updated_at=datetime.now()),
        Content(id=2, internal_id="content2", episode_id=1, title="Content 2", url="url2", content_type="image",
                view_count=50, like_count=5, published_date=datetime.now(), created_at=datetime.now(),
                updated_at=datetime.now())
    ]
    return contents
