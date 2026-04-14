# Google Calendar Setup

This guide walks through connecting the shared calendar to Google Calendar for two-way sync.

## Prerequisites

- A Google account (personal or Workspace)
- Access to Google Cloud Console

## Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (e.g., "General Semantics Calendar")
3. Select the project

## Step 2: Enable the Calendar API

1. Go to **APIs & Services > Library**
2. Search for "Google Calendar API"
3. Click **Enable**

## Step 3: Create OAuth Credentials

1. Go to **APIs & Services > Credentials**
2. Click **Create Credentials > OAuth 2.0 Client ID**
3. If prompted, configure the consent screen first:
   - User type: External (or Internal if using Workspace)
   - App name: "GS HQ Calendar"
   - Add your email as test user
4. Application type: **Desktop app**
5. Download the JSON file

## Step 4: Configure

Place the downloaded credentials file as `calendar/.google_client_secret.json` in this repo.

Then run:

```bash
python scripts/google_calendar_sync.py setup
```

This will open a browser for you to authorize access. The token is stored locally and NOT committed to git.

## Step 5: Create a Shared Calendar

For team use, create a dedicated Google Calendar:

1. In Google Calendar, click **+** next to "Other calendars"
2. Click **Create new calendar**
3. Name it "General Semantics HQ"
4. Share it with team members

Copy the Calendar ID (found in Calendar Settings) and save it:

```bash
echo "YOUR_CALENDAR_ID@group.calendar.google.com" > calendar/.google_calendar_id
```

## Step 6: Sync

```bash
# Push local events to Google Calendar
python scripts/calendar_tool.py push

# Pull Google Calendar events locally
python scripts/calendar_tool.py pull

# Full two-way sync
python scripts/calendar_tool.py sync
```

## Security Notes

- `calendar/.google_client_secret.json` and `calendar/.google_token.json` are in `.gitignore`
- Never commit OAuth tokens to the repo
- Each team member who wants to sync needs their own token (or use a shared service account)
