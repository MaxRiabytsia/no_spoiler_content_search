from shows_api import ShowsAPI
from database import Database
from models import Show

NUMBER_OF_SHOWS_WITH_INFO = 100
NUMBER_OF_SHOWS_WITH_NAME_ONLY = 50_000


def get_n_most_popular_show_info(api, n, name_only=False):
    shows = []
    all_episodes = []
    names = set()
    for i, show_name in enumerate(api.get_n_most_popular_shows(n)):
        if show_name in names:
            continue
        names.add(show_name)

        print(f"Saving {'name' if name_only else 'info'} for show {i + 1}/{n}: {show_name}")
        if name_only:
            show = Show(title=show_name)
            shows.append(show)
        else:
            show, episodes = api.search(show_name)
            if show:
                shows.append(show)
            if episodes:
                all_episodes += episodes

    return shows, all_episodes


def main():
    # api = ShowsAPI()
    # shows, episodes = get_n_most_popular_show_info(api, NUMBER_OF_SHOWS_WITH_INFO)
    # #name_only_shows, _ = get_n_most_popular_show_info(api, NUMBER_OF_SHOWS_WITH_NAME_ONLY, name_only=True)
    # #shows += name_only_shows
    #
    # # save data to file
    # import json
    # with open('show_data.json', 'w') as f:
    #     json.dump([show.dict() for show in shows], f, default=str)
    #
    # with open('episode_data.json', 'w') as f:
    #     json.dump([episode.dict() for episode in episodes], f, default=str)

    # read data from file
    import json
    from models import Show, Episode
    with open('show_data.json', 'r') as f:
        shows = [Show(**show) for show in json.load(f)]

    with open('episode_data.json', 'r') as f:
        episodes = [Episode(**episode) for episode in json.load(f)]

    db = Database()
    db.write(shows)
    db.write(episodes)


if __name__ == "__main__":
    main()
