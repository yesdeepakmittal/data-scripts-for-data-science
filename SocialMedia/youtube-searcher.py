'''
Generate API KEY - https://github.com/yesdeepakmittal/data-scripts/blob/main/API.md#generating-api-key
SET-UP ENV - https://github.com/yesdeepakmittal/data-scripts/blob/main/API.md#setting-up-virtual-environment
'''

from apiclient.discovery import build
import csv

YOUTUBE_API_KEY = ''
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
rows = []

obj = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                        developerKey = YOUTUBE_API_KEY)

params = "id,snippet"
q = 'python'
#type = 'video'  #other - playlist & channel
maxResults = 10
search_result = obj.search().list(q=q,part = params, #type = type, regionCode='US',location ='00.00, 78.6963',locationRadius ='150km',
                                maxResults = maxResults).execute()

for result in search_result.get('items'):
    publishTime = result.get('snippet').get('publishTime')
    channelTitle = result.get('snippet').get('channelTitle')
    channelId = result.get('snippet').get('channelId')
    Description = result.get('snippet').get('description')
    Title = result.get('snippet').get('title')
    
    if result.get('id').get('kind') == 'youtube#video':
        Id = 'videoId - ' + result.get('id').get('videoId')  
    elif result.get('id').get('kind') == 'youtube#playlist':
        Id = 'playlistId - ' + result.get('id').get('playlistId')  
    elif result.get('id').get('kind') == 'youtube#channel':
        Id = 'channelId - ' + result.get('id').get('channelId') 
    else:
        continue
    row = {
        'Id':Id,
        'channelTitle':channelTitle,
        'publishTime':publishTime,
        'channelId':channelId,
        'Title':Title,
        'Description':Description
    }
    rows.append(row)
    
with open('../%s_youtube_searcher.csv'% q ,'w',encoding='utf-8') as f:
    features = ['Id','channelTitle','publishTime','channelId','Title','Description']
    file = csv.DictWriter(f,fieldnames=features)
    file.writeheader()
    for row in rows:
        file.writerow(row)