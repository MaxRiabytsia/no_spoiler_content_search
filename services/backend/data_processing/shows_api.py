from tvdb_v4_official import TVDB
import os
import pandas as pd
from datetime import datetime


class ShowsAPI:
    def __init__(self):
        apikey = os.environ["THETVDB_API_KEY"]
        self._tvdb = TVDB(apikey)

    def search(self, show_name: str, limit: int = 1) -> list[dict]:
        return self._tvdb.search(show_name, type="series", limit=limit)

    def get_show_by_id(self, show_id: int) -> dict:
        return self._tvdb.get_series(show_id)

    def get_updates_since_timestamp(self, timestamp: datetime) -> list[dict]:
        since = int(timestamp.timestamp())
        return self._tvdb.get_updates(since=since, type="series", action="update")

    def get_n_most_popular_shows(self, n: int) -> list[int]:
        df = pd.read_csv("initial_data/shows.csv", encoding="utf-8")
        return df["name"].head(n).tolist()


if __name__ == "__main__":
    # Example usage:
    tvdb_api = ShowsAPI()

    # Get show info by ID
    show_info = tvdb_api.get_show_by_id(121361)
    print(show_info)

    # Search for a show
    search_results = tvdb_api.search("Breaking Bad")
    print(search_results)

    # Get n most popular shows
    n = 5
    most_popular_shows = tvdb_api.get_n_most_popular_shows(n)
    print(most_popular_shows)

