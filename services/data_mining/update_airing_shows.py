from shows_api import ShowsAPI
from database import Database


def get_airing_show_ids(db):
    query = "SELECT internal_id FROM show WHERE is_airing = true"
    return db.read(query)


def get_last_update_timestamp(db):
    query = "SELECT last_run_timestamp FROM pipeline WHERE name = 'update_airing_shows'"
    return db.read(query)


def main():
    api = ShowsAPI()
    db = Database()

    last_update_timestamp = get_last_update_timestamp(db)
    updated_shows = api.get_updates_since_timestamp(last_update_timestamp)
    ids = set(get_airing_show_ids(db))

    updated_data = []
    for show in updated_shows:
        if show["recordId"] in ids:
            # TODO: append only the necessary fields
            show_data = api.get_show_by_id(show["recordId"])
            updated_data.append(show_data)

    db.write("show", updated_data, "upsert", "internal_id")


if __name__ == "__main__":
    main()
