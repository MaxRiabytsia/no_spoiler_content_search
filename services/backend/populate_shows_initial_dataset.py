from shows_api import ShowsAPI
from database import Database
from models import Show, Episode
import json


NUMBER_OF_SHOWS_WITH_INFO = 2_000
NUMBER_OF_SHOWS_WITH_NAME_ONLY = 50_000


def get_n_most_popular_show_info(api, start, end, name_only=False):
    shows = []
    all_episodes = []
    names = set()
    for i, show_name in enumerate(api.get_most_popular_shows(start, end)):
        if show_name in names:
            continue
        names.add(show_name)

        print(f"Saving {'name' if name_only else 'info'} for show {start + i + 1}/{end}: {show_name}")
        if name_only:
            show = Show(title=show_name)
            shows.append(show)
        else:
            try:
                show, episodes = api.search(show_name)
            except Exception as e:
                print(f"Error while getting data for show {show_name}: {e}")
                continue

            if show:
                shows.append(show)
            if episodes:
                all_episodes += episodes

    return shows, all_episodes


def load_files_to_db():
    db = Database()
    for i in range(0, NUMBER_OF_SHOWS_WITH_INFO, 100):
        with open(f'show_data_{i}.json', 'r') as f:
            shows = [Show(**show) for show in json.load(f)]
            db.write(shows)

        with open(f'episode_data_{i}.json', 'r') as f:
            episodes = json.load(f)
            db.write([Episode(**episode) for episode in episodes])

    with open(f'show_data_name_only_{NUMBER_OF_SHOWS_WITH_INFO}.json', 'r') as f:
        shows = [Show(**show) for show in json.load(f)]
        db.write(shows)


def collect_data_to_files():
    api = ShowsAPI()
    for i in range(600, NUMBER_OF_SHOWS_WITH_INFO, 100):
        print(f"Getting data for shows {i + 1}-{i + 100}")
        shows, episodes = get_n_most_popular_show_info(api, i, i + 100)
        with open(f'show_data_{i}.json', 'w') as f:
            json.dump([show.dict() for show in shows], f, default=str)
        with open(f'episode_data_{i}.json', 'w') as f:
            json.dump([episode.dict() for episode in episodes], f, default=str)

    shows, _ = get_n_most_popular_show_info(api, NUMBER_OF_SHOWS_WITH_INFO,
                                            NUMBER_OF_SHOWS_WITH_NAME_ONLY, name_only=True)
    with open(f'show_data_name_only_{NUMBER_OF_SHOWS_WITH_INFO}.json', 'w') as f:
        json.dump([show.dict() for show in shows], f, default=str)


if __name__ == "__main__":
    load_files_to_db()
