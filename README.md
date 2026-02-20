# OpenAIStatusPoller

A lightweight Python script that automatically tracks and logs service updates from the [OpenAI Status Page](https://status.openai.com). Whenever there's a new incident, outage, or degradation — or an update to an existing one — it prints the affected product and latest status message to the console in real time.

---

## How It Works

The script consumes the OpenAI Status RSS/Atom feed and compares each entry against a local in-memory store of previously seen incidents. Instead of blindly re-processing everything on each run, it tracks both the **incident ID** and its **last updated timestamp** — so it catches:

- 🆕 Brand new incidents
- 🔄 Updates to existing incidents (e.g. investigating → monitoring → resolved)
- ✅ Silently skips anything already processed

This approach is efficient, and scales easily — adding a new provider is as simple as adding one line to the `FEEDS` dictionary.

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



## My Approach
**Thought Process & Architectural Exploration**
Initial Direction: Push-Based Architecture

My first instinct was to determine whether OpenAI’s status page exposed any push-based mechanisms. If webhooks, Server-Sent Events, or similar were available, I could design a truly event-driven architecture.

I explored publicly accessible webhook endpoints and other push mechanisms, but none were exposed for the OpenAI status page. Without cooperation from the source, a fully push-based system was not possible.

Exploring HTTP-Level Optimizations

Given that constraint, I moved to polling — but aimed to avoid naive polling.

I investigated HTTP-level conditional request mechanisms such as ETag and Last-Modified, which would allow metadata validation before downloading the full payload. However, the OpenAI status feed does not expose these headers, making conditional GET optimization unavailable.

At this point, I revisited push-based options once more to ensure nothing was missed, including webhook registration attempts — but no programmatic push mechanism was accessible.

Evaluating Slack & Email Integrations

OpenAI’s status page supports Slack and email subscriptions. While these are technically push mechanisms, they introduce external service dependencies between the source and my system.

Architecturally, this does not scale well. Tracking many providers would require managing multiple Slack channels or email routing rules, which shifts complexity elsewhere rather than solving it cleanly.

I chose not to introduce third-party infrastructure unless strictly necessary.

Clarifying the Core Requirement

At one stage, I broadened the problem space toward deeper reliability and failure-mode handling. After reflection, I narrowed the scope back to the assignment’s intent: detecting and handling status updates efficiently — not building a full resilience framework.

This scope correction was intentional.

External Feedback Check

I briefly used AI (Claude) to restate the assignment objective and validate interpretation. The suggested solution included wrapping calls in iterative optimization logic — which I had already considered but deliberately excluded, as it extended beyond what the assignment required.


Final Decision: RSS-Based Polling

RSS emerged as the cleanest and most universal solution:

It requires no authentication or registration.

It is supported across virtually all status providers.

Scaling to multiple providers becomes a configuration problem (adding entries), not an architectural rewrite.

Once I accepted that a request is unavoidable in absence of push support or cache validators, the design simplified significantly.

I prioritized correctness and clarity over over-optimization.


If you have a few minutes, I’d appreciate your thoughts on:

Whether my problem framing and scope discipline were appropriate.

Whether my depth of exploration was justified or excessive.

Where I should tighten my execution style to operate effectively in a fast-moving startup.

I understand time is limited, so even brief written feedback would be great.

chatgpt
https://chatgpt.com/share/6998cdd5-8630-8009-a075-76017cd10d24

claude 
https://claude.ai/share/5f82d4af-2cbf-40f3-b8a1-9e38e28390ab

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

**Timestamps in IST**
All timestamps are converted from UTC/GMT to Indian Standard Time (IST, UTC+5:30) for display.

---

## Limitations

- In-memory state is lost on restart — previously seen incidents will re-print on next run
- Poll interval is set to 60 seconds by default (adjustable in `notify.py`)
- No persistence or UI — console output only (by design)