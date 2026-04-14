# General Semantics HQ

Home base for General Semantics operations, scheduling, and coordination.

## Shared Calendar

The `calendar/` directory is our source of truth for important dates — meetings, demos, events, deadlines.

### Quick Reference

See **[calendar/EVENTS.md](calendar/EVENTS.md)** for all upcoming events in a human-readable format.

The structured data lives in **[calendar/events.json](calendar/events.json)** — this is what syncs with Google Calendar.

### Adding an Event

1. Edit `calendar/events.json` and add your event
2. Run `python scripts/calendar_tool.py render` to regenerate `EVENTS.md`
3. Commit and push

Or use the CLI:

```bash
python scripts/calendar_tool.py add \
  --title "Demo Day" \
  --date "2026-04-25" \
  --time "14:00" \
  --duration 60 \
  --location "Zoom" \
  --description "Monthly demo showcase" \
  --tags "demo,team"
```

### Google Calendar Sync

Once Google Calendar OAuth is configured (see [docs/google-calendar-setup.md](docs/google-calendar-setup.md)), events sync bidirectionally:

```bash
# Push local events to Google Calendar
python scripts/calendar_tool.py push

# Pull Google Calendar events locally  
python scripts/calendar_tool.py pull

# Full two-way sync
python scripts/calendar_tool.py sync
```

### CLI Commands

```bash
python scripts/calendar_tool.py list              # Show upcoming events
python scripts/calendar_tool.py list --past        # Include past events
python scripts/calendar_tool.py add ...            # Add a new event
python scripts/calendar_tool.py remove --id <id>   # Remove an event
python scripts/calendar_tool.py render             # Regenerate EVENTS.md
python scripts/calendar_tool.py push               # Push to Google Calendar
python scripts/calendar_tool.py pull               # Pull from Google Calendar
python scripts/calendar_tool.py sync               # Two-way sync
```
