
# Reddit API Data Collection

This project aims to collect posts from one or more subreddits of your choice using the Reddit API. The collected data is then stored in large files of approximately 10 MB, with a total collection of 500 MB.

## Requirements

To run this project, you will need to have the following installed:

- Python 3.6 or higher
- PRAW Python library
- requests library
- 

## Usage

1. Clone this repository to your local machine.
2. Run 'pipenv shell' to create a virtual dev environment
3. Run 'pipenv install --dev' to install all required dependencies.
4. Open the `main.py` file and add your Reddit API credentials.
5. Select which subreddit you will be crawling and that max file size and total max data size.
6. Run the script and start collecting data.
7. The collected data will be stored in `reddit_data_{file_num}.json` file.

## Requirements
1. Use the reddit API (https://www.reddit.com/dev/api/) to collect posts from one or more subreddits of your choice. You may also add some filters on keywords or users and so on.
2. If a post contains a URL to an HTML page, the title of that page will be added as an additional field to the JSON of the post.
3. The collected data should be stored in files of 10 MB.
4. The aggregate of the files should be at least 500 MB in raw data.

## Notes

- The `main.py` file has several parameters that can be configured, such as `subreddit`, `file_size`, `max_size`.
- By default, the script collects the top posts from all time from the specified subreddit.

