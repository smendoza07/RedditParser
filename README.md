# Reddit Search App with Flask and Lucene

This project consists of two main parts:

1. [Reddit API Data Collection](#reddit-api-data-collection): This script utilizes the Reddit API to collect posts from specified subreddits.
2. [Search Application](#search-application): This Flask application allows users to search through the collected Reddit post data using Apache Lucene for indexing and searching.

## Reddit API Data Collection

This script aims to collect posts from one or more subreddits of your choice using the Reddit API. The collected data is then stored in large files of approximately 10 MB, with a total collection of 500 MB.

### Requirements

To run the data collection script, you will need the following installed:

- Python 3.6 or higher
- PRAW Python library
- requests library
- Beautiful Soup 4
- html library
- os library
- json library

### Usage

1. Clone this repository to your local machine.
2. Run `pipenv shell` to create a virtual development environment.
3. Run `pipenv install --dev` to install all required dependencies.
4. Open the `main.py` file and add your Reddit API credentials.
5. Select which subreddit you will be crawling, the maximum file size per data chunk, and the total maximum data size.
6. Run the script using `python main.py` and start collecting data.

The collected data will be stored in the data folder with filenames like `reddit_data_{subreddit_name}_{file_num}.json`.

### Notes

The `main.py` file has several parameters that can be configured, such as `subreddit`, `file_size`, and `max_size`. By default, the script collects the top posts from all time from a random subreddit until the maximum data size is reached.

## Search Application

This Flask application allows users to search through the collected Reddit post data using Apache Lucene for indexing and searching.

For detailed information on the Search Application functionalities and setup, please refer to the sections below.

- [Functionality](#functionality)
- [Setup](#setup)
- [Code Breakdown](#code-breakdown)
- [Additional Notes](#additional-notes)

This combined approach allows you to collect and manage Reddit post data, and subsequently build a search interface for users to explore the collected information.

## Functionality
- Users can submit a search query through a web interface.
- The application searches the indexed data using Lucene.
- Search results are displayed on the same webpage, including title, score, and a link to the original post (if available).
- The application utilizes a RAMDirectory to store the Lucene index in memory.

## Setup
### Requirements:
- Python 3
- Flask
- Lucene Java library (included in the project)
- A JSON dataset containing Reddit posts (data2 folder in this example)

### Running the application:
1. Ensure you have Python and the required libraries installed.
2. Place the JSON dataset in the `./RedditParser/data2` directory.
3. Run the application from the command line using `python app.py`.
4. Access the application in your web browser at `http://localhost:5000/`.

## Code Breakdown
- `index_corpus` function:
    - Takes a directory path and a Lucene IndexWriter object as input.
    - Iterates through all JSON files in the directory.
    - For each file, reads the JSON data and creates a Lucene document.
    - Extracts title, post URL, body, and comment text from the JSON data and adds them as indexed fields in the document.
    - Adds the document to the Lucene index using the `writer.addDocument` method.
- `search` function:
    - Takes an index directory path, search query, and maximum number of results as input.
    - Opens a Lucene index reader for the specified directory.
    - Creates a Lucene searcher object using the reader.
    - Analyzes the search query using a StandardAnalyzer.
    - Parses the query into a Lucene query object.
    - Performs the search using the searcher and query, retrieving a maximum of the specified number of results.
    - Processes the search results, extracting title, score, and post URL (if available) for each hit.
    - Returns a list of search results in the format (title, score, url).
- `to_html` function:
    - Takes a list of search results as input.
    - Converts the search results into HTML table format.
    - Each row in the table displays the result rank, title (with a link to the original post), and score.
    - Returns the generated HTML code.
- Flask application:
    - The Flask application defines routes for handling user interactions.
    - The `/` route handles GET and POST requests.
        - For GET requests, renders the main search page template (`index.html`).
        - For POST requests, retrieves the search query from the submitted form data.
        - Performs a search using the search function and converts the results to HTML using `to_html`.
        - Renders the `index.html` template again, passing the generated HTML table as a variable.
    - The `/<sinput>` route is an example route that demonstrates processing a URL parameter.
        - In this case, it retrieves the `sinput` value from the URL and performs a search using it.
        - However, this route is not currently used in the application.
- Main execution block:
    - Initializes the Lucene Java Virtual Machine environment.
    - Creates a RAMDirectory instance for storing the Lucene index.
    - Creates a Lucene StandardAnalyzer for text analysis.
    - Configures an IndexWriterConfig object with the analyzer.
    - Creates an IndexWriter object for adding documents to the index.
    - Calls the `index_corpus` function to index the JSON data from the `./RedditParser/data2` directory.
    - Runs the Flask development server, listening for connections on port 5000.

## Additional Notes
- This is a basic example and can be extended to include features like:
    - More sophisticated search query handling and filtering.
    - Pagination for displaying large search result sets.
    - Highlighting search terms within the results.
- The Lucene Java library is included within the project for convenience. You might need to update the library version depending on your requirements.
