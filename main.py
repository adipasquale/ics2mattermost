from ics import Calendar
import requests
import arrow
import click
import locale
from dotenv import load_dotenv
import os
load_dotenv()
locale.setlocale(locale.LC_TIME, "fr_FR")

REQUIRED_ENV_VARIABLES = ["CALENDAR_ICS_URL", "CALENDAR_WEB_URL", "MATTERMOST_HOOK_URL", "MATTERMOST_CHANNEL"]

def event_happens_on_date(event, date):
    return event.begin.date() <= date and event.end.date() >= date


def fetch_events():
    url = os.environ['CALENDAR_ICS_URL']
    return sorted(Calendar(requests.get(url).text).events)

def send_notification(html):
    data = {
      "text": html,
      "icon_emoji": ":calendar:",
      "channel": os.environ["MATTERMOST_CHANNEL"]
    }
    requests.post(os.environ["MATTERMOST_HOOK_URL"], json=data).raise_for_status()

def html_event(event):
    time_str = event.begin.strftime('%Hh%M')
    time_str = "" if time_str == "00h00" else f"{time_str} "
    return f"- {time_str}{event.name}\n"

def build_html_multiple_days(events, days_ahead):
    notif = f"### [Évènements des {days_ahead} prochains jours]({os.environ['CALENDAR_WEB_URL']}) \n\n"
    for offset in range(0, days_ahead):
        day = arrow.now().shift(days=+offset)
        today_str = "Aujourd'hui " if offset == 0 else ""
        notif += f"\n**{today_str}{day.strftime('%A %d %B')}**\n"
        date_events = [e for e in events if event_happens_on_date(e, day.date())]
        if len(date_events) == 0:
            notif += "*Aucun évènement*\n"
        notif += "".join([html_event(e) for e in date_events])
    return notif

def build_html_today(events):
    today_events = [e for e in events if event_happens_on_date(e, arrow.now().date())]
    if len(today_events) == 0:
        return "*Aucun évènement prévu aujourd'hui, quartier libre !*"
    notif = f"**{len(today_events)} évènements aujourd'hui** \n\n"
    notif += "".join([html_event(e) for e in today_events])
    return notif

def validate_env_vars():
    for var_name in REQUIRED_ENV_VARIABLES:
        if not os.environ.get(var_name):
            raise Exception(f"missing environment variable {var_name}")


@click.command()
@click.option("--days-ahead", default=0, help="Include events occuring X days ahead")
def run(days_ahead):
    """Send a summary of upcoming events to Mattermost"""
    events = fetch_events()
    notif = build_html_multiple_days(events, days_ahead) if days_ahead > 0 else build_html_today(events)
    notif += f"\n[Voir le calendrier complet ↗️]({os.environ['CALENDAR_WEB_URL']})"
    send_notification(notif)
    click.echo(f"sent mattermost notif with events!")

if __name__ == '__main__':
    validate_env_vars()
    run()
