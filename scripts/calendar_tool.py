#!/usr/bin/env python3
"""
General Semantics HQ — Shared Calendar Tool

CLI for managing the team's shared calendar. Events are stored in
calendar/events.json and rendered to calendar/EVENTS.md.

Supports Google Calendar sync when OAuth credentials are configured.

Usage:
    python scripts/calendar_tool.py <command> [options]

Commands:
    list        Show upcoming events
    add         Add a new event
    remove      Remove an event by ID
    edit        Edit an existing event
    render      Regenerate EVENTS.md from events.json
    push        Push events to Google Calendar
    pull        Pull events from Google Calendar
    sync        Two-way sync with Google Calendar
"""

import argparse
import json
import os
import sys
import uuid
from datetime import datetime, timedelta
from pathlib import Path

# Resolve paths relative to repo root
REPO_ROOT = Path(__file__).resolve().parent.parent
EVENTS_FILE = REPO_ROOT / "calendar" / "events.json"
EVENTS_MD = REPO_ROOT / "calendar" / "EVENTS.md"
GOOGLE_CONFIG = REPO_ROOT / "calendar" / ".google_calendar_id"


def load_events():
    """Load events from JSON file."""
    if not EVENTS_FILE.exists():
        return {
            "calendar": {
                "name": "General Semantics HQ",
                "timezone": "America/Chicago",
                "description": "Shared calendar for the General Semantics team",
            },
            "events": [],
        }
    with open(EVENTS_FILE) as f:
        return json.load(f)


def save_events(data):
    """Save events to JSON file."""
    EVENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(EVENTS_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def generate_id():
    """Generate a short unique event ID."""
    return uuid.uuid4().hex[:8]


def parse_date(date_str):
    """Parse a date string in various formats."""
    for fmt in ["%Y-%m-%d", "%Y/%m/%d", "%m/%d/%Y", "%m-%d-%Y"]:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Cannot parse date: {date_str}. Use YYYY-MM-DD format.")


def format_event_line(event):
    """Format a single event for display."""
    date = event.get("date", "TBD")
    time = event.get("time", "")
    title = event.get("title", "Untitled")
    location = event.get("location", "")
    duration = event.get("duration_minutes", "")
    tags = event.get("tags", [])

    line = f"  {date}"
    if time:
        line += f" {time}"
    line += f"  {title}"
    if location:
        line += f"  @ {location}"
    if duration:
        line += f"  ({duration} min)"
    if tags:
        line += f"  [{', '.join(tags)}]"
    return line


def cmd_list(args):
    """List upcoming events."""
    data = load_events()
    events = data.get("events", [])

    if not events:
        print("No events scheduled.")
        return

    now = datetime.now().strftime("%Y-%m-%d")

    # Split into upcoming and past
    upcoming = []
    past = []
    for e in events:
        if e.get("date", "9999-99-99") >= now:
            upcoming.append(e)
        else:
            past.append(e)

    # Sort by date, then time
    upcoming.sort(key=lambda e: (e.get("date", ""), e.get("time", "")))
    past.sort(key=lambda e: (e.get("date", ""), e.get("time", "")))

    if upcoming:
        print(f"\n UPCOMING EVENTS ({len(upcoming)})")
        print("=" * 60)
        current_date = None
        for e in upcoming:
            if e.get("date") != current_date:
                current_date = e.get("date")
                try:
                    dt = parse_date(current_date)
                    print(f"\n  {dt.strftime('%A, %B %d, %Y')}")
                except ValueError:
                    print(f"\n  {current_date}")
                print("  " + "-" * 40)
            print(f"    [{e['id']}] {e.get('time', '     ')}  {e['title']}", end="")
            if e.get("location"):
                print(f"  @ {e['location']}", end="")
            if e.get("duration_minutes"):
                print(f"  ({e['duration_minutes']} min)", end="")
            print()
            if e.get("description"):
                print(f"             {e['description']}")
            if e.get("tags"):
                print(f"             tags: {', '.join(e['tags'])}")

    if args.past and past:
        print(f"\n PAST EVENTS ({len(past)})")
        print("=" * 60)
        for e in past:
            print(f"  [{e['id']}] {e.get('date', 'TBD')} {e.get('time', '')}  {e['title']}")

    if not upcoming and not (args.past and past):
        print("No upcoming events.")
    print()


def cmd_add(args):
    """Add a new event."""
    data = load_events()

    event = {
        "id": generate_id(),
        "title": args.title,
        "date": args.date,
        "created": datetime.now().isoformat(),
    }

    if args.time:
        event["time"] = args.time
    if args.duration:
        event["duration_minutes"] = args.duration
    if args.location:
        event["location"] = args.location
    if args.description:
        event["description"] = args.description
    if args.tags:
        event["tags"] = [t.strip() for t in args.tags.split(",")]
    if args.attendees:
        event["attendees"] = [a.strip() for a in args.attendees.split(",")]
    if args.recurring:
        event["recurring"] = args.recurring
    if args.url:
        event["url"] = args.url

    data["events"].append(event)
    save_events(data)

    print(f"Event added: {event['title']} on {event['date']}")
    print(f"ID: {event['id']}")

    # Auto-render
    render_events_md(data)
    print("EVENTS.md updated.")


def cmd_remove(args):
    """Remove an event by ID."""
    data = load_events()
    original_count = len(data["events"])
    data["events"] = [e for e in data["events"] if e.get("id") != args.id]

    if len(data["events"]) == original_count:
        print(f"No event found with ID: {args.id}")
        sys.exit(1)

    save_events(data)
    render_events_md(data)
    print(f"Event {args.id} removed. EVENTS.md updated.")


def cmd_edit(args):
    """Edit an existing event."""
    data = load_events()
    event = None
    for e in data["events"]:
        if e.get("id") == args.id:
            event = e
            break

    if not event:
        print(f"No event found with ID: {args.id}")
        sys.exit(1)

    if args.title:
        event["title"] = args.title
    if args.date:
        event["date"] = args.date
    if args.time:
        event["time"] = args.time
    if args.duration:
        event["duration_minutes"] = args.duration
    if args.location:
        event["location"] = args.location
    if args.description:
        event["description"] = args.description
    if args.tags:
        event["tags"] = [t.strip() for t in args.tags.split(",")]
    if args.url:
        event["url"] = args.url

    event["updated"] = datetime.now().isoformat()
    save_events(data)
    render_events_md(data)
    print(f"Event {args.id} updated. EVENTS.md updated.")


def render_events_md(data=None):
    """Render events.json to EVENTS.md."""
    if data is None:
        data = load_events()

    events = data.get("events", [])
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d")
    cal_name = data.get("calendar", {}).get("name", "General Semantics HQ")

    lines = [
        f"# {cal_name} — Upcoming Events",
        "",
        f"> Auto-generated from events.json — do not edit directly.",
        f"> ",
        f"> Last updated: {now.strftime('%Y-%m-%d %H:%M')}",
        "",
        "---",
        "",
    ]

    upcoming = sorted(
        [e for e in events if e.get("date", "9999") >= now_str],
        key=lambda e: (e.get("date", ""), e.get("time", "")),
    )
    past = sorted(
        [e for e in events if e.get("date", "0000") < now_str],
        key=lambda e: (e.get("date", ""), e.get("time", "")),
        reverse=True,
    )

    if upcoming:
        current_month = None
        for e in upcoming:
            try:
                dt = parse_date(e["date"])
                month_key = dt.strftime("%B %Y")
            except (ValueError, KeyError):
                month_key = "TBD"

            if month_key != current_month:
                current_month = month_key
                lines.append(f"## {month_key}")
                lines.append("")

            time_str = f" at {e['time']}" if e.get("time") else ""
            try:
                dt = parse_date(e["date"])
                date_display = dt.strftime("%a %b %d")
            except (ValueError, KeyError):
                date_display = e.get("date", "TBD")

            lines.append(f"### {e['title']}")
            lines.append(f"- **When:** {date_display}{time_str}")
            if e.get("duration_minutes"):
                lines.append(f"- **Duration:** {e['duration_minutes']} minutes")
            if e.get("location"):
                lines.append(f"- **Where:** {e['location']}")
            if e.get("description"):
                lines.append(f"- **Details:** {e['description']}")
            if e.get("attendees"):
                lines.append(f"- **Attendees:** {', '.join(e['attendees'])}")
            if e.get("url"):
                lines.append(f"- **Link:** {e['url']}")
            if e.get("tags"):
                lines.append(f"- **Tags:** {', '.join(e['tags'])}")
            if e.get("recurring"):
                lines.append(f"- **Recurring:** {e['recurring']}")
            lines.append(f"- *ID: {e['id']}*")
            lines.append("")
    else:
        lines.append("*No upcoming events scheduled.*")
        lines.append("")
        lines.append("Add one with:")
        lines.append("```bash")
        lines.append(
            'python scripts/calendar_tool.py add --title "Event Name" --date "2026-04-20" --time "10:00"'
        )
        lines.append("```")
        lines.append("")

    if past:
        lines.append("---")
        lines.append("")
        lines.append("## Past Events")
        lines.append("")
        for e in past[:10]:  # Show last 10
            time_str = f" at {e['time']}" if e.get("time") else ""
            lines.append(f"- ~~{e.get('date', 'TBD')}{time_str} — {e['title']}~~")
        if len(past) > 10:
            lines.append(f"- *...and {len(past) - 10} more*")
        lines.append("")

    with open(EVENTS_MD, "w") as f:
        f.write("\n".join(lines))


def cmd_render(args):
    """Regenerate EVENTS.md."""
    render_events_md()
    print("EVENTS.md regenerated.")


def cmd_push(args):
    """Push events to Google Calendar."""
    print("Google Calendar push requires OAuth setup.")
    print("See docs/google-calendar-setup.md for instructions.")
    print()
    print("Once configured, this will push all local events to your")
    print("shared Google Calendar.")


def cmd_pull(args):
    """Pull events from Google Calendar."""
    print("Google Calendar pull requires OAuth setup.")
    print("See docs/google-calendar-setup.md for instructions.")
    print()
    print("Once configured, this will import Google Calendar events")
    print("into events.json.")


def cmd_sync(args):
    """Two-way sync with Google Calendar."""
    print("Google Calendar sync requires OAuth setup.")
    print("See docs/google-calendar-setup.md for instructions.")


def main():
    parser = argparse.ArgumentParser(
        description="General Semantics HQ — Shared Calendar Tool"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # list
    p_list = subparsers.add_parser("list", help="Show upcoming events")
    p_list.add_argument("--past", action="store_true", help="Include past events")
    p_list.set_defaults(func=cmd_list)

    # add
    p_add = subparsers.add_parser("add", help="Add a new event")
    p_add.add_argument("--title", required=True, help="Event title")
    p_add.add_argument("--date", required=True, help="Date (YYYY-MM-DD)")
    p_add.add_argument("--time", help="Time (HH:MM, 24h format)")
    p_add.add_argument("--duration", type=int, help="Duration in minutes")
    p_add.add_argument("--location", help="Location or meeting link")
    p_add.add_argument("--description", help="Event description")
    p_add.add_argument("--tags", help="Comma-separated tags")
    p_add.add_argument("--attendees", help="Comma-separated attendees")
    p_add.add_argument(
        "--recurring", help="Recurrence rule (daily, weekly, monthly, or custom)"
    )
    p_add.add_argument("--url", help="Related URL")
    p_add.set_defaults(func=cmd_add)

    # remove
    p_remove = subparsers.add_parser("remove", help="Remove an event")
    p_remove.add_argument("--id", required=True, help="Event ID")
    p_remove.set_defaults(func=cmd_remove)

    # edit
    p_edit = subparsers.add_parser("edit", help="Edit an event")
    p_edit.add_argument("--id", required=True, help="Event ID")
    p_edit.add_argument("--title", help="New title")
    p_edit.add_argument("--date", help="New date (YYYY-MM-DD)")
    p_edit.add_argument("--time", help="New time (HH:MM)")
    p_edit.add_argument("--duration", type=int, help="New duration in minutes")
    p_edit.add_argument("--location", help="New location")
    p_edit.add_argument("--description", help="New description")
    p_edit.add_argument("--tags", help="New tags (comma-separated)")
    p_edit.add_argument("--url", help="New URL")
    p_edit.set_defaults(func=cmd_edit)

    # render
    p_render = subparsers.add_parser("render", help="Regenerate EVENTS.md")
    p_render.set_defaults(func=cmd_render)

    # push
    p_push = subparsers.add_parser("push", help="Push to Google Calendar")
    p_push.set_defaults(func=cmd_push)

    # pull
    p_pull = subparsers.add_parser("pull", help="Pull from Google Calendar")
    p_pull.set_defaults(func=cmd_pull)

    # sync
    p_sync = subparsers.add_parser("sync", help="Two-way sync with Google Calendar")
    p_sync.set_defaults(func=cmd_sync)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
