import praw
import json
import os

# Reddit API credentials
reddit = praw.Reddit(client_id='GUXF6LGTVNbixiD8PPns2Q',
                    client_secret='K2R4WXp5yJUDOpVXSK16mbKx5_b8Ow',
                    user_agent='prawProject',
                    username='OpeningAd5019',
                    password='aPQZWqL&-)vxi)9')

# Maximum size of the JSON file in bytes
max_file_size = 10000 * 1024  # 1 KB

# Maximum size of all JSON files combined in bytes
max_total_size = 100000 * 1024 # 1 MB


# User input of the subreddit to parse
# subreddit_name = input('Enter the name of the subreddit you would like to crawl: ')
subreddit_name = 'python'

# Get the top x posts from the subreddit
posts = reddit.subreddit(subreddit_name).top(limit=None)

# List to store post and comment data
data = []

# Set to keep track of post and comment IDs
post_ids = set()
comment_ids = set()

# Counter for file number
file_num = 1

# Create data folder if it doesn't exist
# if not os.path.exists('data'):
#     os.mkdir('data')

# Loop through each post and its comments
for post in posts:

    # Skip duplicate posts
    if post.id in post_ids:
        continue

    post_data = {
        'title': post.title,
        'url': post.url,
        'author': post.author.name if post.author else None,
        'score': post.score,
        'body': post.selftext,
        'created_utc': post.created_utc,
        'comments': []
    }

    post.comments.replace_more(limit=None)

    for comment in post.comments:
        # Skip duplicate comments
        if comment.id in comment_ids:
            continue

        if isinstance(comment, praw.models.MoreComments):
            continue

        comment_data = {
            'body': comment.body,
            'author': comment.author.name if comment.author else None,
            'score': comment.score,
            'created_utc': comment.created_utc,
            'replies': []
        }

        comment.replies.replace_more(limit=None)

        # Loop through each reply to the comment
        for reply in comment.replies:
            if isinstance(reply, praw.models.MoreComments):
                continue

            reply_data = {
                'body': reply.body,
                'author': reply.author.name if reply.author else None,
                'score': reply.score,
                'created_utc': reply.created_utc
            }

            comment_data['replies'].append(reply_data)

        post_data['comments'].append(comment_data)

        # Add comment ID to set of seen comment IDs
        comment_ids.add(comment.id)

    data.append(post_data)

    # Add post ID to set of seen post IDs
    post_ids.add(post.id)

    # Write the data to a JSON file and check the file size and total size
    file_name = f'reddit_data_{file_num}.json'
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

    file_size = os.path.getsize(file_name)
    total_size = sum(os.path.getsize(f) for f in os.listdir() if f.startswith('reddit_data_'))

    print(f'File name: {file_name}')
    print(f'File size: %.2f MB / %.2f MB' % (file_size/1024/1000, max_file_size/1024/1000))
    print(f'Total size: %.2f MB / %.2f MB' % (total_size/1024/1000, max_total_size/1024/1000))
    print(20*'-')

    if file_size >= max_file_size:
        # Start a new file if the current file size is too large
        file_num += 1
        data = []
    elif total_size >= max_total_size:
        # Stop crawling if the total size of all files is too large
        break
