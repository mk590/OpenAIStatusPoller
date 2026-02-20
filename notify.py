import feedparser
import helper

rss_url = "https://status.openai.com/feed.rss"

feed = feedparser.parse(rss_url)
print(feed)

print("Feed Title:", feed.feed.title)
print("=" * 50)

for entry in feed.entries:
    # print("Title:", entry.title) not needed as per the assignment details 
    # print("Published:", entry.published)
    # print("Summary:", entry.summary)
    print(f"[{entry.published}] {helper.parse_summary(entry.summary)}")
    print("-" * 50)




# the affected product/service, and
# the latest status message or event.