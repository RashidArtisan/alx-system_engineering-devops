def count_words(subreddit, word_list, after=None, word_count={}):
    """Queries the Reddit API recursively, counts occurrences of keywords in hot post titles, and prints the count."""
    import requests

    sub_info = requests.get(
        f"https://www.reddit.com/r/{subreddit}/hot.json",
        params={"after": after},
        headers={"User-Agent": "MyRedditScraper/1.0"},
        allow_redirects=False
    )

    if sub_info.status_code >= 400:
        print(f"Error: HTTP {sub_info.status_code}")
        return

    try:
        info = sub_info.json()
        posts = info.get("data", {}).get("children", [])

        for post in posts:
            title = post.get("data", {}).get("title", "").lower()

            for word in word_list:
                word = word.lower()
                if word in title:
                    word_count[word] = word_count.get(word, 0) + 1

        after = info.get("data", {}).get("after", None)
        if after is None:
            sorted_counts = sorted(word_count.items(), key=lambda x: (-x[1], x[0]))
            for word, count in sorted_counts:
                print(f"{word}: {count}")
            return

        return count_words(subreddit, word_list, after, word_count)

    except (ValueError, KeyError) as e:
        print("Error parsing JSON response:", e)
        return

# Example usage
subreddit_name = "news"
keywords = ["python", "java", "javascript"]
count_words(subreddit_name, keywords)

