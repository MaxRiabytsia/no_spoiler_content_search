from googleapiclient.discovery import build
from datetime import datetime, timedelta
import os
import json


class YoutubeAPI:
    def __init__(self):
        api_key = os.environ['YOUTUBE_API_KEY']
        self._youtube = build('youtube', 'v3', developerKey=api_key)

    def search_videos(self, show_name, min_release_date, max_release_date, limit):
        # TODO: do I need this?
        # Convert min_release_date and max_release_date to ISO format
        min_release_date_iso = (min_release_date - timedelta(
            days=1)).isoformat() + 'Z'  # Subtract 1 day for timezone offset
        max_release_date_iso = (max_release_date + timedelta(days=1)).isoformat() + 'Z'  # Add 1 day for timezone offset

        # Call the YouTube API to search for videos
        request = self._youtube.search().list(
            q=show_name,
            part='snippet',
            type='video',
            publishedAfter=min_release_date_iso,
            publishedBefore=max_release_date_iso,
            maxResults=limit
        )
        response = request.execute()

        return response


if __name__ == '__main__':
    # Example usage
    youtube_api = YoutubeAPI()
    min_release_date = datetime(2011, 6, 19)
    max_release_date = datetime(2012, 4, 1)
    limit = 10
    videos = youtube_api.search_videos("Game of Thrones", min_release_date, max_release_date, limit)

    with open('response_examples/youtube_search_videos_2.json', 'w') as file:
        json.dump(videos, file, indent=4)


