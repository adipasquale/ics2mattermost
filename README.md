# ICS 2 Mattermost

Sends daily and weekly events summaries to Mattermost

<img width="455" alt="Screenshot 2022-04-21 at 18 56 40" src="https://user-images.githubusercontent.com/883348/164512210-ccd906d6-0397-45e6-bc16-81e67375d60e.png">

- This script runs every morning, fetches an ICS calendar from a URL, and sends a webhook notification to Mattermost
- On monday mornings, it generates a notification with all the upcoming week events
- On other weekday mornings, the summary contains only the day events

## Deploy to Scalingo

- Create an app and deploy this repository to it
- Set these environment variables:

```
CALENDAR_ICS_URL="https://blah.com/cal.ics"
CALENDAR_WEB_URL="https://blah.com/cal.html"
MATTERMOST_HOOK_URL="https://mattermost.website/hooks/xxxxx"
MATTERMOST_CHANNEL="some-channel"
```

- scale down the web process, only one-off CRON processes will run

## Dev

- `make install`
- `cp .env.sample .env`
- update env variables in .env
- `make run`
