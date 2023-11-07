import requests

def count_words(subreddit, word_list, after=None, word_count={}):
    if after is None:
        headers = {'User-Agent': 'MyAPI/1.0'}
        params = {'limit': 100}
        response = requests.get(f'https://www.reddit.com/r/{subreddit}/hot.json', headers=headers, params=params)
        if response.status_code != 200:
            return

    data = response.json()
    children = data.get('data', {}).get('children', [])

    for post in children:
        title = post.get('data', {}).get('title', '').lower()
        for word in word_list:
            if word.lower() in title:
                word_count[word] = word_count.get(word, 0) + title.count(word.lower())

    after = data.get('data', {}).get('after', None)

    if after:
        count_words(subreddit, word_list, after, word_count)
    else:
        sorted_words = sorted(word_count.items(), key=lambda item: (-item[1], item[0]))
        for word, count in sorted_words:
            print(f"{word}: {count}")

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 3:
        print("Usage: {} <subreddit> <list of keywords>".format(sys.argv[0]))
        print("Ex: {} programming 'python java javascript'".format(sys.argv[0]))
    else:
        subreddit = sys.argv[1]
        keywords = sys.argv[2].split()
        count_words(subreddit, keywords)
                                                                         
