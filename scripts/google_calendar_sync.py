#!/usr/bin/env python3
"""
Google Calendar Sync for General Semantics HQ

Handles OAuth setup and bidirectional sync between events.json
and a shared Google Calendar.

Requirements:
    pip install google-auth google-auth-oauthlib google-api-python-client

Usage:
    python scripts/google_calendar_sync.py setup          # First-time OAuth
    python scripts/google_calendar_sync.py push            # Local -> Google
    python scripts/google_calendar_sync.py pull            # Google -> Local
    python scripts/google_calendar_sync.py sync            # Two-way sync
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CALENDAR_DIR = REPO_ROOT / "calendar"
EVENTS_FILE = CALENDAR_DIR / "events.json"
CLIENT_SECRET = CALENDAR_DIR / ".google_client_secret.json"
TOKEN_FILE = CALENDAR_DIR / ".google_token.json"
CALENDAR_ID_FILE = CALENDAR_DIR / ".google_calendar_id"

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def check_dependencies():
    """Check if Google API libraries are installed."""
    try:
        import google.auth
        import google_auth_oauthlib.flow
        import googleapiclient.discovery
        return True
    except ImportError:
        print("Missing dependencies. Install with:")
        print("  pip install google-auth google-auth-oauthlib google-api-python-client")
        return False


def get_credentials():
    """Get or refresh OAuth credentials."""
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow

    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CLIENT_SECRET.exists():
                print(f"Client secret not found at {CLIENT_SECRET}")
                print("See docs/google-calendar-setup.md for setup instructions.")
                sys.exit(1)

            flow = InstalledAppFlow.from_client_secrets_file(
                str(CLIENT_SECRET), SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return creds


def get_calendar_service():
    """Build the Google Calendar API service."""
    from googleapiclient.discovery import build
    creds = get_credentials()
    return build("calendar", "v3", credentials=creds)


def get_calendar_id():
    """Get the target Google Calendar ID."""
    if CALENDAR_ID_FILE.exists():
        return CALENDAR_ID_FILE.read_text().strip()
    return "primary"


def load_events():
    """Load local events."""
    if not EVENTS_FILE.exists():
        return {"calendar": {}, "events": []}
    with open(EVENTS_FILE) as f:
        return json.load(f)


def save_events(data):
    """Save local events."""
    with open(EVENTS_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def local_to_google_event(event):
    """Convert a local event to Google Calendar format."""
    tz = "America/Chicago"  # Default timezone

    ge = {
        "summary": event.get("title", "Untitled"),
    }

    date = event.get("date")
    time = event.get("time")
    duration = event.get("duration_minutes", 60)

    if date and time:
        start_dt = f"{date}T{time}:00"
        ge["start"] = {"dateTime": start_dt, "timeZone": tz}
        # Calculate end time
        from datetime import datetime as dt, timedelta
        start = dt.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        end = start + timedelta(minutes=duration)
        ge["end"] = {"dateTime": end.strftime("%Y-%m-%dT%H:%M:%S"), "timeZone": tz}
    elif date:
        ge["start"] = {"date": date}
        ge["end"] = {"date": date}

    if event.get("location"):
        ge["location"] = event["location"]
    if event.get("description"):
        ge["description"] = event["description"]
    if event.get("url"):
        ge["description"] = (ge.get("description", "") + f"\n\nLink: {event['url']}").strip()
    if event.get("attendees"):
        ge["attendees"] = [{"email": a} for a in event["attendees"]]

    # Store local ID in extended properties for sync
    ge["extendedProperties"] = {
        "private": {"gshq_id": event.get("id", "")}
    }

    return ge


def google_to_local_event(ge):
    """Convert a Google Calendar event to local format."""
    import uuid

    event = {
        "id": uuid.uuid4().hex[:8],
        "title": ge.get("summary", "Untitled"),
    }

    start = ge.get("start", {})
    if "dateTime" in start:
        dt_str = start["dateTime"]
        # Parse ISO format
        from datetime import datetime as dt
        try:
            parsed = dt.fromisoformat(dt_str)
            event["date"] = parsed.strftime("%Y-%m-%d")
            event["time"] = parsed.strftime("%H:%M")
        except ValueError:
            event["date"] = dt_str[:10]
    elif "date" in start:
        event["date"] = start["date"]

    end = ge.get("end", {})
    if "dateTime" in end and "dateTime" in start:
        from datetime import datetime as dt
        try:
            s = dt.fromisoformat(start["dateTime"])
            e = dt.fromisoformat(end["dateTime"])
            event["duration_minutes"] = int((e - s).total_seconds() / 60)
        except ValueError:
            pass

    if ge.get("location"):
        event["location"] = ge["location"]
    if ge.get("description"):
        event["description"] = ge["description"]
    if ge.get("attendees"):
        event["attendees"] = [a["email"] for a in ge["attendees"] if "email" in a]

    # Preserve the Google Calendar event ID for future syncs
    event["google_event_id"] = ge.get("id", "")

    # Check if this was originally a local event
    ext = ge.get("extendedProperties", {}).get("private", {})
    if ext.get("gshq_id"):
        event["id"] = ext["gshq_id"]

    event["synced"] = datetime.now().isoformat()

    return event


def cmd_setup():
    """Run OAuth setup."""
    if not check_dependencies():
        sys.exit(1)
    print("Starting OAuth setup...")
    creds = get_credentials()
    print(f"Authenticated! Token saved to {TOKEN_FILE}")
    print(f"Calendar ID: {get_calendar_id()}")


def cmd_push():
    """Push local events to Google Calendar."""
    if not check_dependencies():
        sys.exit(1)

    service = get_calendar_service()
    cal_id = get_calendar_id()
    data = load_events()
    events = data.get("events", [])

    pushed = 0
    for event in events:
        ge = local_to_google_event(event)
        try:
            if event.get("google_event_id"):
                # Update existing
                service.events().update(
                    calendarId=cal_id,
                    eventId=event["google_event_id"],
                    body=ge,
                ).execute()
                print(f"  Updated: {event['title']}")
            else:
                # Create new
                result = service.events().insert(
                    calendarId=cal_id, body=ge
                ).execute()
                event["google_event_id"] = result["id"]
                print(f"  Created: {event['title']}")
            pushed += 1
        except Exception as e:
            print(f"  Error pushing '{event['title']}': {e}")

    save_events(data)
    print(f"\nPushed {pushed}/{len(events)} events to Google Calendar.")


def cmd_pull():
    """Pull events from Google Calendar."""
    if not check_dependencies():
        sys.exit(1)

    service = get_calendar_service()
    cal_id = get_calendar_id()
    data = load_events()

    now = datetime.utcnow().isoformat() + "Z"
    results = (
        service.events()
        .list(calendarId=cal_id, timeMin=now, maxResults=50, singleEvents=True, orderBy="startTime")
        .execute()
    )

    google_events = results.get("items", [])
    existing_google_ids = {
        e.get("google_event_id") for e in data["events"] if e.get("google_event_id")
    }
    existing_local_ids = {e.get("id") for e in data["events"]}

    pulled = 0
    for ge in google_events:
        # Check extended properties for local ID
        ext = ge.get("extendedProperties", {}).get("private", {})
        local_id = ext.get("gshq_id", "")

        if ge["id"] in existing_google_ids:
            continue  # Already synced
        if local_id and local_id in existing_local_ids:
            continue  # Already exists locally

        local_event = google_to_local_event(ge)
        data["events"].append(local_event)
        print(f"  Pulled: {local_event['title']} ({local_event.get('date', 'TBD')})")
        pulled += 1

    save_events(data)
    print(f"\nPulled {pulled} new events from Google Calendar.")


def cmd_sync():
    """Two-way sync."""
    print("=== Pushing local events to Google Calendar ===")
    cmd_push()
    print()
    print("=== Pulling new events from Google Calendar ===")
    cmd_pull()
    print()
    print("Sync complete!")


def main():
    if len(sys.argv) < 2:
        print("Usage: python google_calendar_sync.py <setup|push|pull|sync>")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "setup":
        cmd_setup()
    elif cmd == "push":
        cmd_push()
    elif cmd == "pull":
        cmd_pull()
    elif cmd == "sync":
        cmd_sync()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
