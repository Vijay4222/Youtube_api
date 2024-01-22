from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# YouTube API endpoint for fetching comments

YOUTUBE_API_URL = "https://app.ylytic.com/ylytic/test"
@app.route('/')
def fetch_comments():
    try:
        response = requests.get(YOUTUBE_API_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching comments: {e}")
        return []

def filter_comments(query_params):
    comments_data = fetch_comments()
    result = comments_data

    if 'search_author' in query_params:
        result = [comment for comment in result if query_params['search_author'].lower() in comment['author'].lower()]

    if 'at_from' in query_params and 'at_to' in query_params:
        result = [comment for comment in result if query_params['at_from'] <= comment['at'] <= query_params['at_to']]

    if 'like_from' in query_params and 'like_to' in query_params:
        result = [comment for comment in result if query_params['like_from'] <= comment['like'] <= query_params['like_to']]

    if 'reply_from' in query_params and 'reply_to' in query_params:
        result = [comment for comment in result if query_params['reply_from'] <= comment['reply'] <= query_params['reply_to']]

    if 'search_text' in query_params:
        result = [comment for comment in result if query_params['search_text'].lower() in comment['text'].lower()]

    return result

@app.route('/search', methods=['GET'])
def search_comments():
    query_params = request.args.to_dict()
    
    if not query_params:
        return jsonify({"error": "No search parameters provided"}), 400

    search_result = filter_comments(query_params)
    return jsonify({"comments": search_result})

if __name__ == '__main__':
    app.run(debug=True,port=9091)
