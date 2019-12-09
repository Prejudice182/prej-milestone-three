# Import required modules
from googleapiclient.discovery import build
import os

# Set env variables
DEVELOPER_KEY = os.getenv('DEVELOPER_KEY')
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# Search for a title, and return the first video entry
def youtube_search(query):
    youtube = build(YOUTUBE_API_SERVICE_NAME,
                    YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    search_response = youtube.search().list(q=query, part='id,snippet',
                                            maxResults=1).execute()

    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            result = f"{search_result['id']['videoId']}"

    return result
