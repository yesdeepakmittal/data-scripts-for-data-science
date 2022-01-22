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

obj = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                        developerKey = YOUTUBE_API_KEY)


def get_comments(comments):
    for comment in comments.get('items'):
        comment_id = comment['id']
        comment_text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
        author_name = comment['snippet']['topLevelComment']['snippet']['authorDisplayName']
        author_profile_img = comment['snippet']['topLevelComment']['snippet']['authorProfileImageUrl']
        author_channel = comment['snippet']['topLevelComment']['snippet']['authorChannelUrl']
        like_count = comment['snippet']['topLevelComment']['snippet']['likeCount']
        publishedAt = comment['snippet']['topLevelComment']['snippet']['publishedAt']
        reply_count = comment['snippet']['totalReplyCount']
        row = {
            'comment_id':comment_id,
            'comment_text':comment_text,
            'author_name':author_name,
            'author_profile_img':author_profile_img,
            'author_channel':author_channel,
            'like_count':like_count,
            'publishedAt':publishedAt,
            'reply_count':reply_count
        }
        rows.append(row)

#initial call
comments = obj.commentThreads().list(
                part = 'replies,snippet',
                videoId = '--Enter Video Id Here--',
                maxResults = 100,
    ).execute()

#getting nextpagetoken; None if there is no next page
nextPageToken = comments.get('nextPageToken')

#calling fn for initial call
get_comments(comments)

#if initial call has token for next page then traverse over it
while nextPageToken:
    comments = obj.commentThreads().list(
                part = 'replies,snippet',
                videoId = '--Enter Video Id Here--',
                maxResults = 100,
                pageToken = nextPageToken
    ).execute()
    
    get_comments(comments)
    
    nextPageToken = comments.get('nextPageToken')
    

with open('../all_comments.csv','w',encoding='utf-8') as f:
    features = ['comment_id','comment_text','author_name','author_profile_img','author_channel','like_count','publishedAt','reply_count']
    file = csv.DictWriter(f,fieldnames=features)
    file.writeheader()
    for row in rows:
        file.writerow(row)