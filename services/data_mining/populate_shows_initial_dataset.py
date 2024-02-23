from shows_api import ShowsAPI
from database_query_manager import DatabaseQueryManager


NUMBER_OF_SHOWS_WITH_INFO = 10_000
NUMBER_OF_SHOWS_WITH_NAME_ONLY = 1_000_000


def get_n_most_popular_show_info(api, n, name_only=False):
    data = []
    for show_id in api.get_n_most_popular_show_ids(n):
        if name_only:
            show_name = api.get_show_name(show_id)
            show_info = {"id": show_id, "name": show_name}
        else:
            show_info = api.get_show_info(show_id)

        data.append(show_info)

    return data


def main():
    api = ShowsAPI()
    data = get_n_most_popular_show_info(api, NUMBER_OF_SHOWS_WITH_INFO)
    data += get_n_most_popular_show_info(api, NUMBER_OF_SHOWS_WITH_NAME_ONLY, name_only=True)

    dqm = DatabaseQueryManager()
    dqm.write_shows_data(data)


if __name__ == "__main__":
    main()
