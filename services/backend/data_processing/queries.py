from datetime import datetime


def get_show_by_title_query(title: str) -> dict:
    return {
        "query": {
            "match": {
                "title": title
            }
        }
    }


def get_episodes_by_show_id_query(show_id: int) -> dict:
    return {
        "query": {
            "match": {
                "show_id": show_id
            }
        }
    }


def get_content_query(query: str, start_date: datetime, end_date: datetime) -> dict:
    return {
        "query": {
            "bool": {
                "must": [
                    {
                        "multi_match": {
                            "query": query,
                            "fields": ["title", "description", "channel_name"]
                        }
                    },
                    {
                        "range": {
                            "air_date": {
                                "gte": start_date,
                                "lte": end_date
                            }
                        }
                    }
                ]
            }
        }
    }


def get_episode_data_query(episode_id: int) -> dict:
    return {
        "query": {
            "match": {
                "id": episode_id
            }
        }
    }


def get_airing_show_ids_query():
    return {
        "query": {
            "term": {
                "is_airing": True
            }
        },
        "_source": ["external_id"]
    }


def get_last_update_timestamp_query():
    return {
        "query": {
            "term": {
                "name": "update_airing_shows"
            }
        },
        "_source": ["last_run_timestamp"]
    }
