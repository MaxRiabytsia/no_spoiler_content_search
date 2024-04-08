import json

from shows_api import ShowsAPI
from database import Database

NUMBER_OF_SHOWS_WITH_INFO = 1_000
NUMBER_OF_SHOWS_WITH_NAME_ONLY = 50_000


def get_n_most_popular_show_info(api, n, name_only=False):
    data = []
    for i, show_name in enumerate(api.get_n_most_popular_shows(n)):
        if name_only:
            show_info = {"name": show_name}
            if show_info:
                data.append(show_info)
        else:
            show_info = api.search(show_name)
            if show_info:
                show_info = show_info[0]
                data.append({
                    'internal_id': show_info['id'],
                    'title': show_info['name'],
                    'description': show_info['overview'],
                    'poster_url': show_info['image_url'],
                    'is_airing': show_info['status'] == 'Continuing',  # TODO: Check if this is correct
                })

        if i % 100 == 0:
            print(f"Processed {i} shows")
            with open("initial_data/shows_data.json", "w") as f:
                json.dump(data, f, indent=2)

    return data


def main():
    api = ShowsAPI()
    data = get_n_most_popular_show_info(api, NUMBER_OF_SHOWS_WITH_INFO)
    data += get_n_most_popular_show_info(api, NUMBER_OF_SHOWS_WITH_NAME_ONLY, name_only=True)

    db = Database()
    db.write("show", data)


if __name__ == "__main__":
    main()
