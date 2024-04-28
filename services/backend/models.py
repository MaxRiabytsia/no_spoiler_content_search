from typing import Optional, Type, Any, Tuple
from copy import deepcopy
from datetime import datetime

from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo


def partial_model(model: Type[BaseModel]):
    def make_field_optional(field: FieldInfo, default: Any = None) -> Tuple[Any, FieldInfo]:
        new = deepcopy(field)
        new.default = default
        new.annotation = Optional[field.annotation]  # type: ignore
        return new.annotation, new
    return create_model(
        f'Partial{model.__name__}',
        __base__=model,
        __module__=model.__module__,
        **{
            field_name: make_field_optional(field_info)
            for field_name, field_info in model.__fields__.items()
        }
    )


class ESBaseModel(BaseModel):
    def to_es_loadable_object(self):
        raise NotImplementedError


@partial_model
class Show(ESBaseModel):
    external_id: int
    title: str
    description: str
    image_url: str
    is_airing: bool
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    @classmethod
    def from_api_object(cls, api_object):
        return cls(
            external_id=api_object["tvdb_id"],
            title=api_object["name"],
            description=api_object["overview"],
            image_url=api_object["thumbnail"],
            is_airing=api_object["status"] == "Continuing",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    def to_es_loadable_object(self):
        return {
            '_index': 'show',
            'external_id': self.external_id,
            'title': self.title,
            'description': self.description,
            'image_url': self.image_url,
            'is_airing': self.is_airing,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


@partial_model
class Episode(ESBaseModel):
    external_id: int
    name: str
    show_external_id: int
    season: int
    number_in_season: int
    number_in_show: int
    is_last_of_the_season: bool
    is_last_of_the_show: bool
    description: str
    image_url: str
    air_date: datetime
    next_episode_air_date: datetime
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    @classmethod
    def from_api_object(cls, api_object: dict, show_external_id: str, number_in_show: int, next_episode_air_date: str = None):
        return cls(
            external_id=api_object["id"],
            name=api_object["name"],
            show_external_id=show_external_id,
            season=api_object["seasonNumber"],
            number_in_season=api_object["number"],
            number_in_show=number_in_show,
            is_last_of_the_season=api_object["finaleType"] == "season",
            is_last_of_the_show=api_object["finaleType"] == "series",
            description=api_object["overview"],
            image_url=api_object["image"],
            air_date=datetime.strptime(api_object["aired"], "%Y-%m-%d"),
            next_episode_air_date=datetime.strptime(next_episode_air_date, "%Y-%m-%d") if next_episode_air_date else None,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    def to_es_loadable_object(self):
        return {
            '_index': 'episode',
            'external_id': self.external_id,
            'name': self.name,
            'show_external_id': self.show_external_id,
            'season': self.season,
            'number_in_season': self.number_in_season,
            'number_in_show': self.number_in_show,
            'is_last_of_the_season': self.is_last_of_the_season,
            'is_last_of_the_show': self.is_last_of_the_show,
            'description': self.description,
            'image_url': self.image_url,
            'air_date': self.air_date.isoformat(),
            'next_episode_air_date': self.next_episode_air_date.isoformat() if self.next_episode_air_date else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


@partial_model
class Content(ESBaseModel):
    external_id: int
    episode_external_id: int
    title: str
    channel_name: str
    description: str
    url: str
    image_url: str
    published_date: datetime
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    @classmethod
    def from_youtube_api_object(cls, youtube_api_object: dict, episode_external_id: str):
        return cls(
            external_id=youtube_api_object["id"]["videoId"],
            episode_external_id=episode_external_id,
            title=youtube_api_object["snippet"]["title"],
            channel_name=youtube_api_object["snippet"]["channelTitle"],
            description=youtube_api_object["snippet"]["description"],
            url=f"https://www.youtube.com/watch?v={youtube_api_object['id']['videoId']}",
            image_url=youtube_api_object["snippet"]["thumbnails"]["high"]["url"],
            published_date=datetime.strptime(youtube_api_object["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%SZ"),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    def to_es_loadable_object(self):
        return {
                '_index': 'content',
                'external_id': self.external_id,
                'episode_external_id': self.episode_external_id,
                'title': self.title,
                'channel_name': self.channel_name,
                'url': self.url,
                'image_url': self.image_url,
                'published_date': self.published_date.isoformat(),
                'created_at': self.created_at.isoformat(),
                'updated_at': self.updated_at.isoformat()
            }
