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
                "show_external_id": show_id
            }
        },
        "size": 10000
    }


def get_episode_data_query(episode_id: int) -> dict:
    return {
        "query": {
            "match": {
                "external_id": episode_id
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
