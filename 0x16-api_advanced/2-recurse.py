#!/usr/bin/python3
"""Module for task 2"""

def recurse(subreddit, hot_list=[], count=0, after=None):
    """Queries the Reddit API and returns all hot posts
    of the subreddit"""
    import requests

    try:
        sub_info = requests.get(
            f"https://www.reddit.com/r/{subreddit}/hot.json",
            params={"limit": 25, "count": count, "after": after},
            headers={"User-Agent": "MyRedditScraper/1.0"},
            allow_redirects=False
        )
        
        if sub_info.status_code >= 400:
            print(f"Error: HTTP {sub_info.status_code}")
            return None

        info = sub_info.json()

        hot_l = hot_list + [child.get("data").get("title")
                            for child in info.get("data").get("children")]

        if not info.get("data").get("after"):
            return hot_l

        return recurse(subreddit, hot_l, info.get("data").get("count"),
                       info.get("data").get("after"))

    except requests.exceptions.RequestException as e:
        print("Error making the request:", e)
        return None
    except (ValueError, KeyError) as e:
        print("Error parsing JSON response:", e)
        return None

# Example usage
subreddit_name = "news"
hot_titles = recurse(subreddit_name)

if hot_titles is None:
    print("Invalid subreddit or no results found.")
else:
    for i, title in enumerate(hot_titles, start=1):
        print(f"{i}. {title}")

