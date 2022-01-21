#https://api.stackexchange.com/docs

import requests
import csv
rows = []

response = requests.get('http://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow')
for i in response.json()['items']:
    tags = str(i['tags'])
    title = i['title']
    link = i['link']
    question_id = i['question_id']
    view_count = i['view_count']
    is_answered = i['is_answered']
    owner = i['owner']['display_name']
    owner_id = i['owner']['user_id']
    
    row = {
        'tags':tags,
        'title':title,
        'link':link,
        'question_id':question_id,
        'view_count':view_count,
        'is_answered':is_answered,
        'owner':owner,
        'owner_id':owner_id
    }
    rows.append(row)

with open('../stackoverflow_questions.csv','w',encoding='utf-8') as f:
    features = ['tags','title','link','question_id','view_count','is_answered','owner','owner_id']
    file = csv.DictWriter(f,fieldnames=features)
    file.writeheader()
    for row in rows:
        file.writerow(row)