from pydantic import BaseModel
from datetime import datetime


class ESBaseModel(BaseModel):
    def to_es_loadable_object(self):
        raise NotImplementedError


class Show(ESBaseModel):
    id: int
    internal_id: str
    title: str
    description: str
    rating: float
    image_url: str
    is_airing: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_api_object(cls, api_object):
        return cls(
            internal_id=api_object["id"],
            title=api_object["seriesName"],
            description=api_object["overview"],
            rating=api_object["siteRating"],
            image_url=api_object["banner"],
            is_airing=api_object["status"] == "Continuing",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    def to_es_loadable_object(self):
        return {
            '_index': 'shows',
            '_id': self.id,
            'id': self.id,
            'internal_id': self.internal_id,
            'title': self.title,
            'description': self.description,
            'rating': self.rating,
            'image_url': self.image_url,
            'is_airing': self.is_airing,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Episode(ESBaseModel):
    id: int
    internal_id: str
    name: str
    show_id: int
    season: int
    number_in_season: int
    number_in_show: int
    is_last_of_the_season: bool
    is_last_of_the_show: bool
    description: str
    image_url: str
    air_date: datetime
    next_episode_air_date: datetime
    created_at: datetime
    updated_at: datetime


class Content(ESBaseModel):
    id: int
    internal_id: str
    episode_id: int
    title: str
    channel_name: str
    url: str
    image_url: str
    published_date: datetime
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_youtube_api_object(cls, youtube_api_object):
        return cls(
            internal_id=youtube_api_object["id"]["videoId"],
            title=youtube_api_object["snippet"]["title"],
            channel_name=youtube_api_object["snippet"]["channelTitle"],
            url=f"https://www.youtube.com/watch?v={youtube_api_object['id']['videoId']}",
            image_url=youtube_api_object["snippet"]["thumbnails"]["high"]["url"],
            published_date=datetime.strptime(youtube_api_object["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%SZ"),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    def to_es_loadable_object(self):
        return {
                '_index': 'content',
                '_id': self.id,
                'id': self.id,
                'internal_id': self.internal_id,
                'episode_id': self.episode_id,
                'title': self.title,
                'channel_name': self.channel_name,
                'url': self.url,
                'image_url': self.image_url,
                'published_date': self.published_date.isoformat(),
                'created_at': self.created_at.isoformat(),
                'updated_at': self.updated_at.isoformat()
            }
