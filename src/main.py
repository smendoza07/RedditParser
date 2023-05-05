import praw
import json
import os
import requests
from bs4 import BeautifulSoup
import html
import prawcore

def get_comment_data(comment):
    # Recursively gets data for a comment and its replies.
    comment_data = {
        'body': comment.body,
        'author': comment.author.name if comment.author else None,
        'id': comment.id,
        'parent_id': comment.parent_id,
        'score': comment.score,
        'created_utc': comment.created_utc,
        'replies': [],
    }
    comment.replies.replace_more(limit=None)
    for reply in comment.replies:
        if isinstance(reply, praw.models.MoreComments):
            reply = reply.comments()[0]
        reply_data = get_comment_data(reply)
        comment_data['replies'].append(reply_data)
    return comment_data

# Reddit API credentials
reddit = praw.Reddit(client_id='GUXF6LGTVNbixiD8PPns2Q',
                    client_secret='K2R4WXp5yJUDOpVXSK16mbKx5_b8Ow',
                    user_agent='prawProject',
                    username='OpeningAd5019',
                    password='aPQZWqL&-)vxi)9')

# Change the values in () to change the total size
# 100 = 100KB, 1000 = 1MB, 10000 = 10 MB, 100000 = 100 MB
# Maximum size of all JSON files combined in bytes
max_total_size = (500000) * 1024

# Create data folder if it doesn't exist
if not os.path.exists('data'):
    os.mkdir('data')

# List to store post and comment data
data = []

# Set to keep track of post and comment IDs
post_ids = set()
comment_ids = set()

# Set to keep track of hyperlinks
hyperlinks = []
link_titles = []

while True:

    # Get a random subreddit
    subreddit_name = reddit.random_subreddit(nsfw=False).display_name

    # Get the top x posts from the subreddit
    posts = reddit.subreddit(subreddit_name).top(limit=None)

    # Loop through each post and its comments
    for post in posts:

        html_body = post.selftext_html

        # Decode the HTML and extract all hyperlinks
        if html_body:
            text_body = html.unescape(html_body)
            hyperlinks = [link['href'] for link in BeautifulSoup(text_body, 'html.parser').find_all('a')]

        # If there is no HTML, set hyperlinks to empty lists
        else:
            hyperlinks = []

        # Skip duplicate posts
        if post.id in post_ids:
            continue
        
        # Get post data
        post_data = {
            'title': post.title,
            'post_id': post.id,
            'post_url': f"https://www.reddit.com{post.permalink}",
            'author': post.author.name if post.author else None,
            'body': post.selftext,
            'url': post.url,
            'score': post.score,
            'upvote_ratio': post.upvote_ratio,
            'created_utc': post.created_utc,
            'num_comments': post.num_comments,
            'links': [ [link for link in hyperlinks],
                        ],
            'comments': []
        }

        # Get comment data
        post.comments.replace_more(limit=None)

        for comment in post.comments.list():
            # Skip duplicate comments
            if comment.id in comment_ids:
                continue
            # Skip MoreComments objects
            if isinstance(comment, praw.models.MoreComments):
                comment = comment.comments()[0]
            # Get comment data
            comment_data = get_comment_data(comment)
            # Add comment data to post data
            post_data['comments'].append(comment_data)

            # Add comment ID to set of seen comment IDs
            comment_ids.add(comment.id)

        # Add post ID to set of seen post IDs
        post_ids.add(post.id)

        # Write the data to a JSON file and check the file size and total size
        file_name = f'data/reddit_data_{subreddit_name}_{post.id}.json'
        with open(file_name, 'w') as f:
            json.dump(post_data, f, indent=4)

        # Get the file size and total size
        data_folder = 'data'
        
        # file_size = os.path.getsize(file_name)
        total_size = sum(os.path.getsize(os.path.join(data_folder, f)) for f in os.listdir(data_folder))

        if total_size >= max_total_size:
            # Stop crawling if the total size of all files is too large
            break

    # Check if total size limit is reached
    total_size = sum(os.path.getsize(os.path.join(data_folder, f)) for f in os.listdir(data_folder))
    if total_size >= max_total_size:
        break

print('Data collection complete.')
