# Reddit Data Collection Project

## Overview
This project is designed to collect and analyze Reddit posts and comments from various political subreddits. The data is scraped using Reddit's API and stored in a local MongoDB database for further analysis. The project uses Python for data collection, and MongoDB for data storage.

---

## Tech Stack
* `Python` - The project is developed and tested using Python v3.9.7. [Python Website](https://www.python.org/)  
* `time` - Provides various time-related functions. [Python Documentation](https://docs.python.org/3/library/time.html)  
* `datetime` - Supplies classes for manipulating dates and times. [Python Documentation](https://docs.python.org/3/library/datetime.html)  
* `requests` - A simple HTTP library for Python. [Requests Documentation](https://requests.readthedocs.io/en/latest/)  
* `pymongo` - A Python distribution containing tools for working with MongoDB. [PyMongo Documentation](https://pymongo.readthedocs.io/en/stable/)  
* `MongoDB Community Server` - Used for storing Reddit data locally. It supports ad-hoc queries, secondary indexing, and real-time aggregations. Includes MongoDB Compass, a GUI for querying and analyzing data. [Download MongoDB](https://www.mongodb.com/try/download/community)  

---

## Data Source Documentation

### Subreddits
Data is collected from the following subreddits:

* [r/politics](https://reddit.com/r/politics) - News and discussion about U.S. politics  
* [r/uselection](https://reddit.com/r/uselection) - Discussion about U.S. elections  
* [r/news](https://reddit.com/r/news) - News articles about current events in the United States and the rest of the world  
* [r/democrats](https://reddit.com/r/democrats) - The Democratic Party's daily news updates, policy analysis, links, and opportunities to participate in the political process  
* [r/republican](https://reddit.com/r/republican) - Partisan subreddit for Republicans to discuss issues with other Republicans  
* [r/conservative](https://reddit.com/r/conservative) - Subreddit for conservatives, both fiscal and social, to read and discuss political and cultural issues from a distinctly conservative point of view  
* [r/worldnews](https://reddit.com/r/worldnews) - A place for major news from around the world, excluding US-internal news.  
* [r/americanpolitics](https://reddit.com/r/americanpolitics) - A place to discuss the American political process, parties, politicians, and topics  
* [r/Liberal](https://reddit.com/r/Liberal) - A subreddit to discuss Liberal ideas including politics  
* [r/StateOfTheUnion](https://reddit.com/r/StateOfTheUnion) - A subreddit to discuss current political agendas and topics  

### Sorting Options
The project fetches posts using the following sorting options:  
* `/new` - New posts on subreddits  
* `/hot` - Posts gaining rapid upvotes/comments  
* `/rising` - Newly submitted posts rapidly getting engagement  

The sort options are stored in `sort_options.txt`.

---

## Files Description

1. **subreddits.txt**  
   Contains a list of subreddits to scrape, one per line.  
   Example:  
   ```txt
   politics
   uselection
   news
   democrats
   republican
   conservative
   worldnews
   americanpolitics
   Liberal
   StateOfTheUnion

2. **sort_options.txt**  
   Specifies sorting criteria for collecting posts.  
   Example:
   ```txt
   new
   hot
   rising

3. **login_cred.txt**  
   Contains Reddit API credentials in the following format:  
   ```txt
   client_id=<your_id>  
   secret_key=<your_key>  
   user_agent=<your_agent>  

## System Architecture for Data Collection

The project uses the following steps to collect data:

1. **Authenticate** with the Reddit API using `client_id`, `secret_key`, and `user_agent`.
2. **Fetch posts** from specified subreddits using different sorting options (`new`, `hot`, `rising`).
3. **Insert posts and comments** into a MongoDB collection if they do not already exist.

For more details on the Reddit API:

* [Reddit API Documentation](https://www.reddit.com/dev/api/)
* [Reddit API Archive](https://github.com/reddit-archive/reddit/wiki/API)

## How to Run the Project

1. Install required Python libraries:  
   ```bash
   pip install requests pymongo
2. Ensure MongoDB is running locally.
3. Add your Reddit API credentials to `login_cred.txt`.
4. Run the main script:
   ```bash
   python reddit.py
5. The collected data will be stored in the MongoDB collections `posts` and `comments`.
