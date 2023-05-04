import praw
import json
import os
import requests
from bs4 import BeautifulSoup
import html
import prawcore

# Reddit API credentials
reddit = praw.Reddit(client_id='GUXF6LGTVNbixiD8PPns2Q',
                    client_secret='K2R4WXp5yJUDOpVXSK16mbKx5_b8Ow',
                    user_agent='prawProject',
                    username='OpeningAd5019',
                    password='aPQZWqL&-)vxi)9')

# Maximum size of the JSON file in bytes
max_file_size = 100 * 1024  # 1 KB

# Maximum size of all JSON files combined in bytes
max_total_size = 1000 * 1024 # 1 MB

# Create data folder if it doesn't exist
if not os.path.exists('data'):
    os.mkdir('data')

# List to store post and comment data
data = []

# Set to keep track of post and comment IDs
post_ids = set()

hyperlinks = []
link_title = ''

while True:

    # Counter for file number
    file_num = 1

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
            
            # For each hyperlink, send a GET request to the URL and extract the page title
            for link in hyperlinks:
                try:
                    response = prawcore.requests.get(link, timeout=5,)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    link_title = soup.title.string.strip()
                except:
                    link_title = [f"Could not get title"]
        else:
            hyperlinks = []
            link_title = ''

        if post.id in post_ids:
            continue

        post_data = {
            'title': post.title,
            'post_url': f"https://www.reddit.com{post.permalink}",
            'author': post.author.name if post.author else None,
            'url': post.url,
            'links': { 'title': link_title,
                    'link': [link for link in hyperlinks],
                    },
        }

        data.append(post_data)

        # Add post ID to set of seen post IDs
        post_ids.add(post.id)

        # Write the data to a JSON file and check the file size and total size
        file_name = f'data/reddit_data_{subreddit_name}_{file_num}.json'
        with open(file_name, 'w') as f:
            json.dump(data, f, indent=4)

        data_folder = 'data'
        file_size = os.path.getsize(file_name)
        total_size = sum(os.path.getsize(os.path.join(data_folder, f)) for f in os.listdir(data_folder))

        if file_size >= max_file_size:
            # Start a new file if the current file size is too large
            file_num += 1
            data = []
        if total_size >= max_total_size:
            # Stop crawling if the total size of all files is too large
            break

    # Check if total size limit is reached
    total_size = sum(os.path.getsize(os.path.join(data_folder, f)) for f in os.listdir(data_folder))
    if total_size >= max_total_size:
        break
