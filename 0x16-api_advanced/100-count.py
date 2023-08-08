import json
import requests

def count_words(subreddit, word_list, after=None, count=None):
    if after is None:
        count = [0] * len(word_list)

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {'user-agent': 'bhalut'}
    params = {'after': after} if after else None

    response = requests.get(url, params=params, headers=headers, allow_redirects=False)

    if response.status_code == 200:
        data = response.json()

        for topic in data['data']['children']:
            title_words = topic['data']['title'].split()
            for word in title_words:
                word = word.lower().rstrip('.,!?_')
                if word in word_list:
                    index = word_list.index(word)
                    count[index] += 1

        after = data['data']['after']
        if after is None:
            combined_words = {}
            for i, word in enumerate(word_list):
                word = word.lower()
                if word in combined_words:
                    combined_words[word] += count[i]
                else:
                    combined_words[word] = count[i]

            sorted_words = sorted(combined_words.items(), key=lambda x: (-x[1], x[0]))

            for word, count in sorted_words:
                print(f"{word}: {count}")
        else:
            count_words(subreddit, word_list, after, count)

# Example usage
subreddit = "python"
keywords = ["python", "code", "programming"]
count_words(subreddit, keywords)

