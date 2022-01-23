'''
This program returns all the videos of a youtube channel in a date range


Generate API KEY - https://github.com/yesdeepakmittal/data-scripts/blob/main/API.md#generating-api-key
SET-UP ENV - https://github.com/yesdeepakmittal/data-scripts/blob/main/API.md#setting-up-virtual-environment
'''

from apiclient.discovery import build
import csv
rows = []

channelId = '--Enter Channel Id Here--'

#specify date range here
publishedAfter = '2019-09-01T00:00:00Z',
publishedBefore = '2022-01-01T00:00:00Z',

YOUTUBE_API_KEY = ''
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

obj = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                        developerKey = YOUTUBE_API_KEY)

#print(help(obj.search().list))

def get_video_stats(videoId):
    #help(obj.videos().list)
    video_result = obj.videos().list(
            part='statistics,contentDetails,status',
            id=videoId,
            fields = 'items(contentDetails(duration,definition),status(madeForKids),statistics(viewCount,likeCount,favoriteCount,commentCount))'
                ).execute().get('items')[0]

    duration = video_result['contentDetails']['duration']
    definition = video_result['contentDetails']['definition']
    madeForKids = video_result['status']['madeForKids']
    viewCount = video_result['statistics']['viewCount']
    likeCount = video_result['statistics']['likeCount']
    favoriteCount = video_result['statistics']['favoriteCount']
    commentCount = video_result['statistics']['commentCount']

    hash = {
        'duration':duration,
        'definition':definition,
        'madeForKids':madeForKids,
        'viewCount':viewCount,
        'likeCount':likeCount,
        'favoriteCount':favoriteCount,
        'commentCount':commentCount,
    }
    return hash

def get_videos(videos):
    from html import unescape
    for video in videos.get('items'):
        videoId = video['id']['videoId']
        publishedAt = video['snippet']['publishedAt']
        title = video['snippet']['title']
        description = video['snippet']['description']
        channelTitle = video['snippet']['channelTitle']

        vStats = get_video_stats(videoId)

        row = {
            'videoId':videoId,
            'publishedAt':publishedAt,
            'title':unescape(title),  #example &quot; -> "
            'description':description,
            'channelTitle':channelTitle,

            'duration':vStats['duration'],
            'definition':vStats['definition'],
            'madeForKids':vStats['madeForKids'],
            'viewCount':vStats['viewCount'],
            'likeCount':vStats['likeCount'],
            'favoriteCount':vStats['favoriteCount'],
            'commentCount':vStats['commentCount'],
        }
        rows.append(row)
        

#initial call 
videos = obj.search().list(
            part='snippet',
            channelId=channelId,
            order = 'viewCount',
            maxResults=5,
            publishedAfter = publishedAfter,
            publishedBefore = publishedBefore
            # fields = 'items(id(videoId),snippet(title,publishedAt,description,channelTitle))' #bcoz not returning nextPageToken
            ).execute()

nextPageToken = videos.get('nextPageToken')

get_videos(videos)

while nextPageToken:
    videos = obj.search().list(
            part='snippet',
            channelId=channelId,
            order = 'viewCount',
            maxResults=5,
            publishedAfter = publishedAfter,
            publishedBefore = publishedBefore,
            pageToken = nextPageToken
            ).execute()

    get_videos(videos)

    nextPageToken = videos.get('nextPageToken')


with open('../all_videos.csv','w',encoding='utf-8') as f:
    features = ['videoId','publishedAt','title','description','channelTitle',
                'duration','definition','madeForKids','viewCount','likeCount','favoriteCount','commentCount']
    file = csv.DictWriter(f,fieldnames=features)
    file.writeheader()
    for row in rows:
        file.writerow(row)