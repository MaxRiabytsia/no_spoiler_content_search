from pydantic import BaseModel
from datetime import datetime


class Show(BaseModel):
    id: int
    internal_id: str
    title: str
    description: str
    rating: float
    poster_url: str
    is_airing: bool
    created_at: datetime
    updated_at: datetime


class Episode(BaseModel):
    id: int
    internal_id: str
    name: str
    show_id: int
    season: int
    number: int
    is_last_of_the_season: bool
    is_last_of_the_show: bool
    description: str
    air_date: datetime
    next_episode_air_date: datetime
    created_at: datetime
    updated_at: datetime


class Content(BaseModel):
    id: int
    internal_id: str
    episode_id: int
    title: str
    url: str
    content_type: str
    view_count: int
    like_count: int
    published_date: datetime
    created_at: datetime
    updated_at: datetime
