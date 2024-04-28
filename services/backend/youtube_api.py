from googleapiclient.discovery import build
from datetime import datetime, timedelta
import os
import json

from models import Content


class YoutubeAPI:
    def __init__(self):
        api_key = os.environ['YOUTUBE_API_KEY']
        self._youtube = build('youtube', 'v3', developerKey=api_key)

    def search_videos(self, query: str, min_release_date: datetime, max_release_date: datetime,
                      episode_id: id, limit: int = 50):
        # TODO: do I need this? do I need to add a timezone offset?
        # Convert min_release_date and max_release_date to ISO format
        min_release_date_iso = (min_release_date - timedelta(
            days=1)).isoformat() + 'Z'  # Subtract 1 day for timezone offset
        max_release_date_iso = (max_release_date + timedelta(days=1)).isoformat() + 'Z'  # Add 1 day for timezone offset

        request = self._youtube.search().list(
            q=query,
            part='snippet',
            type='video',
            publishedAfter=min_release_date_iso,
            publishedBefore=max_release_date_iso,
            maxResults=limit
        )
        response = request.execute()

        if response['items']:
            content_results = [Content.from_youtube_api_object(item, episode_id) for item in response['items']]
            return content_results

        return []


if __name__ == '__main__':
    # Example usage
    youtube_api = YoutubeAPI()
    min_date = datetime(2011, 6, 19)
    max_date = datetime(2012, 4, 1)
    videos = youtube_api.search_videos("Game of Thrones", min_date, max_date, 10)

    with open('response_examples/youtube_search_videos_2.json', 'w') as file:
        json.dump(videos, file, indent=4)


