import requests

def count_words(subreddit, word_list, after=None, word_count=None):
    if word_count is None:
        word_count = {}

    sub_info = requests.get(
        f"https://www.reddit.com/r/{subreddit}/hot.json",
        params={"after": after},
        headers={"User-Agent": "My-User-Agent"},
        allow_redirects=False
    )

    if sub_info.status_code != 200:
        return

    info = sub_info.json()

    hot_l = [child.get("data").get("title")
             for child in info
             .get("data")
             .get("children")]

    if not hot_l:
        return

    for title in hot_l:
        split_words = title.split(' ')
        for word in word_list:
            for s_word in split_words:
                normalized_word = s_word.lower().strip('!._')
                if normalized_word == word.lower():
                    if word in word_count:
                        word_count[word] += 1
                    else:
                        word_count[word] = 1

    if not info.get("data").get("after"):
        sorted_counts = sorted(word_count.items(), key=lambda kv: (-kv[1], kv[0].lower()))
        for k, v in sorted_counts:
            print('{}: {}'.format(k.lower(), v))
    else:
        count_words(subreddit, word_list, info.get("data").get("after"), word_count)

""" Example usage"""
subreddit = "programming"
word_list = ["python", "java", "javascript"]
count_words(subreddit, word_list)

