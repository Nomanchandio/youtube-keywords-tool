import json
from googleapiclient.discovery import build


api_key = 'AIzaSyAVZhXNtFnRkq0Dzx8WZLTd4hxRo-w98q4'
youtube = build('youtube', 'v3', developerKey=api_key)

def get_related_keywords(keyword):
    search_response = youtube.search().list(
        q=keyword,
        type='video',
        part='snippet',
        maxResults=50 
    ).execute()


    related_keywords = []
    for item in search_response.get('items', []):
        snippet = item.get('snippet', {})
        title = snippet.get('title', '')

        related_keywords.extend(title.split())

    related_keywords = list(set([keyword.lower() for keyword in related_keywords]))

    return related_keywords

def lambda_handler(event, context):
    if 'queryStringParameters' in event:
        keyword = event['queryStringParameters'].get('keyword', '')
    else:
        keyword = ''

    print("Received keyword:", keyword)


    related_keywords = get_related_keywords(keyword)

    print("Related keywords:", related_keywords)


    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(related_keywords)
    }

    return response

# Test lambda_handler locally
if __name__ == '__main__':
    test_event = {
        "queryStringParameters": {
            "keyword": "school"
        }
    }
    print(lambda_handler(test_event, None))