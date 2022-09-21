import praw
import pandas as pd
import csv
from tabulate import tabulate

def init_reddit():
    """Initialize a reddit instance using a username and password from the
    "reddit_login.txt" file and a client and secret key from the "api_keys.txt"
    file.

    returns:
        reddit_obj: Reddit instance created for the user.
    """
    with open('reddit_login.txt', 'r') as i:
        login_list = list(csv.reader(i))[0]
        username = login_list[0]
        password = login_list[1]
    with open('api_keys.txt', 'r') as i:
        key_list = list(csv.reader(i))[0]
        client_id = key_list[0]
        secret_key = key_list[1]
    
    reddit_obj = praw.Reddit(username=username,
                         password=password,
                         client_id=client_id,
                         client_secret=secret_key,
                         user_agent='small_feed_0.0.1'
    )
    return reddit_obj

def get_subscribed(reddit_obj) -> list:
    """Get the user's subscribed subreddits using a reddit instance and
    return a list of subreddits.

    Args:
        reddit_obj: Reddit instance created for the user.
    Returns:
        sub_list: List of subreddits.
    """
    sub_list = reddit_obj.get('/subreddits/mine/subscriber')
    return sub_list

def print_small_feed(reddit_obj, sub_list) -> None:
    """Print a table of the top 3 posts from the past 24 hours
    from each subreddit in a list.

    Args:
        reddit_obj: Reddit instance created for the user.
        sub_list: List of subreddit names.
    """
    df = pd.DataFrame()
    titles=[]
    subreddits=[]
    scores=[]
    num_comments=[]
    urls=[]
    for name in sub_list:
        for post in name.top(time_filter="day", limit=3):
            titles.append(post.title)
            subreddits.append(name.display_name)
            scores.append(post.score)
            num_comments.append(post.num_comments)
            urls.append('https://www.reddit.com' + post.permalink)
    df['Title'] = titles
    df['Subreddit'] = subreddits
    df['Scores'] = scores
    df['Comments'] = num_comments
    df['Url'] = urls
    with pd.option_context('display.max_rows', None,
                       'display.max_columns', None
                       ):
        print(df)
                        
def main() -> None:
    """Use "reddit_login.txt" and "api_keys.txt" to access PRAW and display a small reddit feed.
    """
    reddit = init_reddit()
    subreddits = get_subscribed(reddit)
    print_small_feed(reddit, subreddits)

if __name__ == '__main__':
    main()
