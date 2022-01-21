'''
Generate API KEY - https://github.com/yesdeepakmittal/data-scripts/blob/main/API.md#generating-api-key
SET-UP ENV - https://github.com/yesdeepakmittal/data-scripts/blob/main/API.md#setting-up-virtual-environment
'''

from apiclient.discovery import build

YOUTUBE_API_KEY = ''
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

obj = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                        developerKey = YOUTUBE_API_KEY)

playlist = obj.playlistItems().list(
                    part='id,snippet',
                    playlistId='--Enter Playlist Id here--',
                    maxResults=20).execute()
with open('../playlist.txt','w',encoding='utf-8') as f:
    for video in playlist.get('items'):
        print(video['snippet']['description'],file=f)
        print('-'*100,file=f)