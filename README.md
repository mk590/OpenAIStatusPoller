# OpenAIStatusPoller

A lightweight Python script that automatically tracks and logs service updates from the [OpenAI Status Page](https://status.openai.com). Whenever there's a new incident, outage, or degradation — or an update to an existing one — it prints the affected product and latest status message to the console in real time.

---

## How It Works

The script consumes the OpenAI Status RSS/Atom feed and compares each entry against a local in-memory store of previously seen incidents. Instead of blindly re-processing everything on each run, it tracks both the **incident ID** and its **last updated timestamp** — so it catches:

- 🆕 Brand new incidents
- 🔄 Updates to existing incidents (e.g. investigating → monitoring → resolved)
- ✅ Silently skips anything already processed

This approach is efficient, event-driven in nature, and scales easily — adding a new provider is as simple as adding one line to the `FEEDS` dictionary.

---

## Example Output

```
[2026-02-18 22:10:22] 🆕 NEW | Product: OpenAI - Elevated error rate in Chat Completions
Status: We are currently investigating elevated error rates affecting Chat Completions API users.

[2026-02-18 22:25:10] 🔄 UPDATE | Product: OpenAI - Elevated error rate in Chat Completions
Status: We have identified the root cause and a fix is being deployed.

[2026-02-18 22:40:55] 🔄 UPDATE | Product: OpenAI - Elevated error rate in Chat Completions
Status: This incident has been resolved.
```

---

## Project Structure

```
OpenAIStatusPoller/
│
├── helper.py          # Utility functions (summary parser, IST time converter)
├── notify.py          # Core logic — feed checker, polling loop, incident tracking
└── README.md
```

---

## Setup & Installation

**1. Clone the repo**
```bash
git clone https://github.com/your-username/OpenAIStatusPoller.git
cd OpenAIStatusPoller
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run**
```bash
python notify.py
```

---

## Dependencies

```
feedparser
pytz

Readme · MD
Copy

# OpenAIStatusPoller

A lightweight Python script that automatically tracks and logs service updates from the [OpenAI Status Page](https://status.openai.com). Whenever there's a new incident, outage, or degradation — or an update to an existing one — it prints the affected product and latest status message to the console in real time.

---

## How It Works

The script consumes the OpenAI Status RSS/Atom feed and compares each entry against a local in-memory store of previously seen incidents. Instead of blindly re-processing everything on each run, it tracks both the **incident ID** and its **last updated timestamp** — so it catches:

- 🆕 Brand new incidents
- 🔄 Updates to existing incidents (e.g. investigating → monitoring → resolved)
- ✅ Silently skips anything already processed

This approach is efficient, event-driven in nature, and scales easily — adding a new provider is as simple as adding one line to the `FEEDS` dictionary.

---

## Example Output

```
[2026-02-18 22:10:22] 🆕 NEW | Product: OpenAI - Elevated error rate in Chat Completions
Status: We are currently investigating elevated error rates affecting Chat Completions API users.

[2026-02-18 22:25:10] 🔄 UPDATE | Product: OpenAI - Elevated error rate in Chat Completions
Status: We have identified the root cause and a fix is being deployed.

[2026-02-18 22:40:55] 🔄 UPDATE | Product: OpenAI - Elevated error rate in Chat Completions
Status: This incident has been resolved.
```

---

## Project Structure

```
OpenAIStatusPoller/
│
├── helper.py          # Utility functions (summary parser, IST time converter)
├── notify.py          # Core logic — feed checker, polling loop, incident tracking
└── README.md
```

---

## Setup & Installation

**1. Clone the repo**
```bash
git clone https://github.com/your-username/OpenAIStatusPoller.git
cd OpenAIStatusPoller
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run**
```bash
python notify.py
```

---

## Dependencies

```
feedparser
pytz
beautifulsoup4
```

Install manually if needed:
```bash
pip install feedparser pytz beautifulsoup4
```

---

## Adding More Status Pages

The script is built to scale. To track additional providers, add them to the `FEEDS` dict in `notify.py`:

```python
FEEDS = {
    "OpenAI":    "https://status.openai.com/history.rss",
    ...
}
```



---

## Design Decisions

*Note*
If time constraints allow you to provide feedback I would be grateful to have one , otherwise i acknowledge the time and energy constraints of startups


**My Approach**
My first instinct was to figure out whether the OpenAI status page supported any push-based mechanism so I could build a truly event-driven architecture. I explored webhooks, Server-Sent Events, and other push notification methods — but none of them were publicly accessible on OpenAI's status page. Without a push mechanism from the source, a fully event-driven architecture wasn't possible.
This led me to polling. But rather than polling blindly, I looked into HTTP-level optimizations like ETag and Last-Modified headers — these would let me make a lightweight metadata request first and only fetch the full payload if something had actually changed. Unfortunately, the OpenAI status feed doesn't send these headers, so that optimization wasn't available either.
Then went back to check if by any means any kind of push notifications are available 
Tried registering with the webhooks but no response from OpenAI
At that point I considered Slack and email integrations — OpenAI's status page does support native subscriptions for both. But that would mean inserting an external service between OpenAI and my program, which adds unnecessary dependency and doesn't scale. If I needed to track 100 providers, I'd need 100 Slack channels or email filters — which clearly isn't a real engineering solution.
Then i pasted the same assigment description to claude and asked what the assignment wants and the resonse shows a for loop that wraps my call and do some optimization before final output which i already thought of but avoided as i thought it is not asked.
RSS feed turned out to be the right answer. It's universally available across virtually every status page provider, requires no registration or authentication, and the scalability problem reduces to just adding a new entry to a dictionary. -- but his as per me is obvious. 

Well i enjoyed the assignment and figuring out things, i am attaching both chatgpt and claude chats for your reference 

If time constraints allow you to provide feedback I would be grateful to have one , otherwise i acknowledge the time and energy constraints of startups
- what i did right and wrong from start to end , problem comphrension , drifting away from core problem etc, 
- as per the chats , did i take more help from AI than needed or i am slow while moving things as a YC startup i feel you guys can help me to know which areas i should improve 
- a voice note as feedback will also work great , just open the chats attached and record the thoughts, i am comfortable in both hindi and english 
chatgpt
https://chatgpt.com/share/6998cdd5-8630-8009-a075-76017cd10d24
claude 
https://claude.ai/share/5f82d4af-2cbf-40f3-b8a1-9e38e28390ab


**Timestamps in IST**
All timestamps are converted from UTC/GMT to Indian Standard Time (IST, UTC+5:30) for display.

---

## Limitations

- In-memory state is lost on restart — previously seen incidents will re-print on next run
- Poll interval is set to 60 seconds by default (adjustable in `notify.py`)
- No persistence or UI — console output only (by design)