from shows_api import ShowsAPI
from database import Database
from data_processing.queries import get_airing_show_ids_query, get_last_update_timestamp_query


def get_airing_show_ids(db):
    query = get_airing_show_ids_query()
    res = db.read(query, "show")
    return [hit["_source"]["external_id"] for hit in res["hits"]["hits"]]


def get_last_update_timestamp(db):
    query = get_last_update_timestamp_query()
    res = db.read(query, "pipeline")

    if len(res["hits"]["hits"]) > 0:
        last_run_timestamp = res["hits"]["hits"][0]["_source"]["last_run_timestamp"]
    else:
        last_run_timestamp = None

    return last_run_timestamp


def main():
    api = ShowsAPI()
    db = Database()

    last_update_timestamp = get_last_update_timestamp(db)
    updated_shows = api.get_updates_since_timestamp(last_update_timestamp)
    ids = set(get_airing_show_ids(db))

    for show in updated_shows:
        if show["recordId"] in ids:
            show = api.get_show_by_id(show["recordId"])
            print(f"Updating show {show.name}...")
            episodes = api.get_episodes_by_show_id(show.external_id)
            db.write([show])
            db.write(episodes)


if __name__ == "__main__":
    main()
