from youtube_api import YoutubeAPI
from database import Database

NUMBER_OF_SHOWS_TO_COLLECT_INFO_FOR = 100
NUMBER_OF_VIDEOS_TO_COLLECT = 50


def get_season_end_episode_data(db):
    query = f"""
                SELECT e.id, s.name AS show_name, e.air_date, e.next_episode_air_date
                FROM show s
                JOIN episode e ON s.id = e.show_id
                WHERE e.is_last_episode_of_the_season = true
                ORDER BY s.rating DESC
                LIMIT {NUMBER_OF_SHOWS_TO_COLLECT_INFO_FOR}
            """
    return db.read(query)


def main():
    api = YoutubeAPI()
    db = Database()

    episodes = get_season_end_episode_data(db)
    for episode in episodes:
        videos = api.search_videos(episode['show_name'],
                                   min_release_date=episode['air_date'],
                                   max_release_date=episode['next_episode_air_date'],
                                   limit=NUMBER_OF_VIDEOS_TO_COLLECT)
        videos["episode_id"] = episode["id"]
        db.write("content", videos, "insert", "internal_id")


if __name__ == "__main__":
    main()
