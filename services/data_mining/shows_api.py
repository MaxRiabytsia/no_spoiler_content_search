from tvdb_v4_official import TVDB
import os


class ShowsAPI:
    def __init__(self):
        apikey = os.environ["THETVDB_API_KEY"]
        self._tvdb = TVDB(apikey)

    def get_show_info(self, show_id: int) -> dict:
        return self._tvdb.get_series(show_id)

    def get_show_name(self, show_id: int) -> str:
        show_info = self.get_show_info(show_id)
        return show_info["name"]

    def get_n_most_popular_show_ids(self, n: int) -> list[int]:
        pass


if __name__ == "__main__":
    # Example usage:
    tvdb_api = ShowsAPI()

    # Get show info by ID
    show_info = tvdb_api.get_show_info(121361)
    print(show_info)

    # Get show name by ID
    show_name = tvdb_api.get_show_name(70908)
    print(show_name)
