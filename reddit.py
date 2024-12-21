import requests
import pymongo
import time
from datetime import datetime, timezone

# MongoDB setup
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
reddit_db = mongo_client["RedditDB"]
reddit_posts = reddit_db["posts"]
reddit_comments = reddit_db["comments"]

# Helper function to read text files
def read_file(filepath):
    with open(filepath) as file:
        return [line.strip() for line in file]

# Load Reddit credentials and scraping settings
reddit_creds = {
    k: v
    for k, v in (line.split('=') for line in read_file('login_cred.txt'))
}
subreddits_to_scrape = read_file('subreddits.txt')
reddit_sort_options = read_file('sort_options.txt')

# Authenticate Reddit API
def authenticate_reddit():
    print("Authenticating with Reddit...")
    auth = requests.auth.HTTPBasicAuth(reddit_creds['client_id'], reddit_creds['secret_key'])
    headers = {'User-Agent': reddit_creds['user_agent']}
    try:
        response = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth,
                                 data={'grant_type': 'client_credentials'}, headers=headers)
        if response.status_code == 200:
            headers['Authorization'] = f"bearer {response.json()['access_token']}"
            print("Authenticated with Reddit successfully.")
            return headers
        else:
            print(f"Authentication failed: {response.status_code}")
    except Exception as e:
        print(f"Error authenticating: {e}")
    return None

# Fetch Reddit posts and insert into MongoDB
def fetch_reddit_posts(headers):
    base_url = 'https://oauth.reddit.com'
    for subreddit in subreddits_to_scrape:
        for sort_option in reddit_sort_options:
            url = f'{base_url}/r/{subreddit}/{sort_option}'
            try:
                response = requests.get(url, headers=headers, params={'limit': 100})
                if response.status_code == 200:
                    for post in response.json()['data']['children']:
                        post_data = post['data']
                        post_json = {
                            "_id": post_data['id'],
                            "subreddit": post_data['subreddit'],
                            "created_utc": datetime.utcfromtimestamp(post_data['created_utc']).isoformat(),
                            "title": post_data['title'],
                            "upvote_ratio": post_data['upvote_ratio'],
                            "num_comments": post_data['num_comments'],
                            "url": post_data['url'],
                            "postid": post_data['id'],
                            "upvotes": post_data['ups']
                        }
                        # Insert into MongoDB if it doesn't already exist
                        if not reddit_posts.find_one({"_id": post_json['_id']}):
                            reddit_posts.insert_one(post_json)
                            print(f"Inserted post {post_json['_id']}")
                        fetch_reddit_comments(post_data['permalink'], post_json['_id'], headers)
                        time.sleep(2)
            except Exception as e:
                print(f"Error fetching posts: {e}")

# Fetch Reddit comments for a post and insert into MongoDB
def fetch_reddit_comments(permalink, post_id, headers):
    try:
        response = requests.get(f'https://oauth.reddit.com{permalink}', headers=headers)
        if response.status_code == 200:
            for comment in response.json()[1]['data']['children']:
                comment_data = comment['data']
                comment_json = {
                    "_id": comment_data['id'],
                    "subreddit": comment_data['subreddit'],
                    "created_utc": datetime.utcfromtimestamp(comment_data['created_utc']).isoformat(),
                    "post_id": post_id,
                    "comment_id": comment_data['id'],
                    "text": comment_data['body']
                }
                # Insert into MongoDB if it doesn't already exist
                if not reddit_comments.find_one({"_id": comment_json['_id']}):
                    reddit_comments.insert_one(comment_json)
                    print(f"Inserted comment {comment_json['_id']}")
                time.sleep(2)
    except Exception as e:
        print(f"Error fetching comments: {e}")

# Main function to start data collection
def main():
    headers = authenticate_reddit()
    if headers:
        fetch_reddit_posts(headers)

if __name__ == "__main__":
    main()
