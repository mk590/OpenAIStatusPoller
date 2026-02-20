import requests

rss_url = "https://status.openai.com/feed.rss"


response = requests.get(rss_url)

with open('example.txt', 'a') as file:
    file.write(response.text)
