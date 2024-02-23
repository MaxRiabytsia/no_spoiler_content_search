import datetime

from youtube_api import YoutubeAPI
from database import Database


def get_episodes_without_next_episode_air_date(db):
    query = """
                SELECT e.id, s.name AS show_name, e.air_date, e.next_episode_air_date, e.updated_at
                FROM show s
                JOIN episode e ON s.id = e.show_id
                WHERE e.next_episode_air_date IS NULL
            """
    return db.read(query)


def data_should_be_updated(updated_at, air_date, next_episode_air_date):
    """
    We should update data periodically. The update schedule should grow longer with the passage of time
    For example, if the last episode was released within last month, we should update data daily,
    but if the last episode was released more than 6 months ago, then we should update it once a month.

    :param updated_at: the last time the data was updated
    :param air_date: the air date of the episode
    :param next_episode_air_date: the air date of the next episode
    :return: True if the data should be updated, False otherwise
    """
    # TODO: issue: it takes time to update data, the schedule should be adjusted to account for that. It might
    #  lead when we update data only every second time we should.

    # if the next episode has already aired, and we have updated the data after that, we don't need to update anymore
    if next_episode_air_date and next_episode_air_date < updated_at:
        return False

    today = datetime.date.today()

    # if the episode has aired more than 6 months ago, we should update it once a month
    if air_date < today - datetime.timedelta(days=180):
        return updated_at < today - datetime.timedelta(days=30)

    # if the episode has aired more than 1 month ago, we should update it once a week
    if air_date < today - datetime.timedelta(days=30):
        return updated_at < today - datetime.timedelta(days=7)

    # if the episode has aired within last month, we should update it daily
    return updated_at < today - datetime.timedelta(days=1)


def main():
    api = YoutubeAPI()
    db = Database()

    ids = get_episodes_without_next_episode_air_date(db)
    for episode in ids:
        if data_should_be_updated(episode["updated_at"], episode["air_date"], episode["next_episode_air_date"]):
            # TODO: should I use updated_at or air_date as min_release_date?
            videos = api.search_videos(episode['show_name'],
                                       min_release_date=episode['air_date'],
                                       max_release_date=episode['next_episode_air_date'],
                                       limit=50)
            videos["episode_id"] = episode["id"]
            db.write("content", videos, "insert", "internal_id")


if __name__ == "__main__":
    main()
