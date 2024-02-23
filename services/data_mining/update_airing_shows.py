from shows_api import ShowsAPI
from database import Database


def get_airing_show_ids(db):
    query = "SELECT internal_id FROM show WHERE is_airing = true"
    return db.read(query)


def main():
    api = ShowsAPI()
    db = Database()

    ids = get_airing_show_ids(db)
    for show_id in ids:
        show_info = api.get_show_info(show_id)
        db.write("show", show_info, "upsert", "internal_id")


if __name__ == "__main__":
    main()
