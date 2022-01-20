'''
- Create a Virtual environment first - https://gist.github.com/yesdeepakmittal/61494217c8be4a7e61524e27824943bd
- install this library - https://github.com/googleapis/google-api-python-client
- https://github.com/googleapis/google-api-python-client#windows

OR
- Read this - https://github.com/yesdeepakmittal/data-scripts/blob/main/API.md#setting-up-virtual-environment
'''

from apiclient.discovery import build
YOUTUBE_API_KEY = ''
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

obj = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                        developerKey = YOUTUBE_API_KEY)
params = "id,snippet"
q = 'Kunal Kushwaha'
search_result = obj.search().list(q=q,part = params,
                                maxResults = 10).execute()

flag = False
for result in search_result.get('items',[]):
    if result.get('snippet').get('title') == q:
        id = result.get('snippet').get('channelId')
        flag = True
        break

if flag:
    print(id)
else:
    print('Invalid Channel Name')