from tvdb_v4_official import TVDB
import os
import pandas as pd
from datetime import datetime

from models import Show, Episode


class ShowsAPI:
    def __init__(self):
        apikey = os.environ["THETVDB_API_KEY"]
        self._tvdb = TVDB(apikey)

    def search(self, show_name: str, limit: int = 1) -> tuple[Show, list[Episode]] or None:
        show_data = self._tvdb.search(show_name, type="series", limit=limit)
        print(show_data)

        if not show_data:
            return None, []

        show = Show.from_api_object(show_data[0])
        episodes_data = self._tvdb.get_series_episodes(show.external_id)
        print(episodes_data)
        episodes = []
        if episodes_data:
            episode_number_in_show = 0
            air_date = None
            for episode in episodes_data["episodes"]:
                if episode["seasonNumber"] == 0 or not episode["aired"]:
                    continue

                episode = Episode.from_api_object(episode, show.external_id, episode_number_in_show)
                air_date = episode.air_date

                if episodes:
                    episodes[-1].next_episode_air_date = air_date

                episodes.append(episode)
                episode_number_in_show += 1

            episodes[-1].next_episode_air_date = air_date

        return show, episodes

    def get_show_by_id(self, show_id: int) -> dict:
        return self._tvdb.get_series(show_id)

    def get_updates_since_timestamp(self, timestamp: datetime) -> list[dict]:
        since = int(timestamp.timestamp())
        return self._tvdb.get_updates(since=since, type="series", action="update")

    def get_n_most_popular_shows(self, n: int) -> list[int]:
        df = pd.read_csv("data_processing/initial_data/shows.csv", encoding="utf-8")
        return df["name"].head(n).tolist()


if __name__ == "__main__":
    # Example usage:
    tvdb_api = ShowsAPI()

    # # Get show info by ID
    # show_info = tvdb_api.get_show_by_id(121361)
    # print(show_info)
    #
    # # Search for a show
    # search_results = tvdb_api.search("Breaking Bad")
    # print(search_results)
    #
    # # Get n most popular shows
    # n = 5
    # most_popular_shows = tvdb_api.get_n_most_popular_shows(n)
    # print(most_popular_shows)

    apikey = os.environ["THETVDB_API_KEY"]
    tvdb = TVDB(apikey)
    series = tvdb.search("House of dragon", type="series", limit=1)
    import json
    with open("data_processing/response_examples/get_search_house_of_dragon.json", "w") as f:
        json.dump(series, f, indent=4)

