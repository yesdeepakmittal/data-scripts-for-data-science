'''
Generate API KEY - https://github.com/yesdeepakmittal/data-scripts/blob/main/API.md#generating-api-key
SET-UP ENV - https://github.com/yesdeepakmittal/data-scripts/blob/main/API.md#setting-up-virtual-environment
'''

from apiclient.discovery import build
import csv
rows = []

YOUTUBE_API_KEY = ''
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

nextPageToken = None #assign nextPageToken from search result to get all playlists beyond query limit

obj = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                        developerKey = YOUTUBE_API_KEY)

search_result = obj.playlists().list(part='contentDetails,snippet',
                                channelId='--Enter Channel Id Here--',
                                maxResults=50, #pageToken = nextPageToken
                            ).execute()

for playlist in search_result.get('items'):
    playlist_id = playlist['id']
    playlist_title = playlist['snippet']['title']
    playlist_videos_count = playlist['contentDetails']['itemCount']
    playlist_description = playlist['snippet']['description']
    playlist_published_at = playlist['snippet']['publishedAt']

    row = {
        'playlist_id':playlist_id,
        'playlist_title':playlist_title,
        'playlist_videos_count':playlist_videos_count,
        'playlist_description':playlist_description,
        'playlist_published_at':playlist_published_at,
    }
    rows.append(row)

with open('../all_playlists.csv','w',encoding='utf-8') as f:
    features = ['playlist_id','playlist_title','playlist_videos_count','playlist_description','playlist_published_at']
    file = csv.DictWriter(f,fieldnames=features)
    file.writeheader()
    for row in rows:
        file.writerow(row)