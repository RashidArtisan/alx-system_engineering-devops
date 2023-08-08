#!/usr/bin/python3
"""Module for task 2"""
def recurse(subreddit, hot_list=[], after=None):
    """Queries the Reddit API recursively and returns all hot post titles of the subreddit"""
    import requests

    sub_info = requests.get(
        f"https://www.reddit.com/r/{subreddit}/hot.json",
        params={"after": after},
        headers={"User-Agent": "MyRedditScraper/1.0"},
        allow_redirects=False
    )

    if sub_info.status_code >= 400:
        print(f"Error: HTTP {sub_info.status_code}")
        return None

    try:
        info = sub_info.json()
        posts = info.get("data", {}).get("children", [])

        if not posts:
            return hot_list

        hot_list.extend([post.get("data", {}).get("title", "") for post in posts])

        after = info.get("data", {}).get("after", None)
        if after is None:
            return hot_list
        else:
            return recurse(subreddit, hot_list, after)

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


