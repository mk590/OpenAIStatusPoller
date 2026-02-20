import feedparser
import helper
import time
import pytz
from datetime import datetime

FEEDS = {
    "OpenAI": "https://status.openai.com/feed.rss",
}


IST = pytz.timezone("Asia/Kolkata")

def to_ist(published_str):
    published_str = published_str.replace("GMT", "+0000")
    dt_utc = datetime.strptime(published_str, "%a, %d %b %Y %H:%M:%S %z")
    dt_ist = dt_utc.astimezone(IST)
    return dt_ist.strftime("%Y-%m-%d %H:%M:%S")


seen_entries = {}

def check_feed(provider, url):
    feed = feedparser.parse(url)
    for entry in feed.entries:
        entry_id = entry.id
        # feedparser normalizes updated time into a struct_time tuple
        entry_updated = entry.get("updated", entry.get("published", None))

        if entry_id not in seen_entries or seen_entries[entry_id] != entry_updated:
            seen_entries[entry_id] = entry_updated
            print(f"[{to_ist(entry.published)}] {helper.parse_summary(entry.summary)}")

        

        

while True:
    for provider, url in FEEDS.items():
        check_feed(provider, url)
    time.sleep(60)