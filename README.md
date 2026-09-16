# Yazke Lead Finder

A Claude Code skill that finds real, fully-contactable local business leads and writes them into a Google Sheet shared with Logan. Runs on your own Claude Code account and credits — nothing here depends on Logan's Discord bot, his API keys, or his Google account.

## Setup — just ask Claude to do it

Open this folder in Claude Code and say something like **"set this up for me"**. Claude can handle almost all of it directly: installing the Python packages, running the first login, checking everything connects. Point it at this README and it'll walk through each step below with you.

**One step Claude genuinely can't do for you**: creating your own Google OAuth client (step 2 below) has to happen in your own browser, logged into your own Google account — that's Google requiring a real human click-through for identity/consent reasons, not something any AI can do on your behalf. Claude can tell you exactly what to click, but you do the clicking.

### 1. Install Python dependencies

```
pip install -r requirements.txt
```

### 2. Get your own free Google OAuth client (the one manual step)

This lets the sheet-writer script log into **your own** Google account — nothing of Logan's.

1. Go to https://console.cloud.google.com and create a new project (e.g. "Yazke Lead Finder")
2. Go to "APIs & Services" → "Library" and enable:
   - **Google Sheets API**
   - **Google Drive API**
3. Go to "APIs & Services" → "Credentials" → "Create Credentials" → "OAuth client ID"
   - If prompted, configure the consent screen first: choose "External", fill in an app name and your email, save through the defaults
   - Application type: **Desktop app**
   - Name it anything (e.g. "Yazke Lead Finder")
   - Click Create
4. Download the JSON file, rename it to `oauth_credentials.json`, and place it in this same folder

### 3. Get added to the shared sheet

Ask Logan to share the "Agency Leads" Google Sheet with your Google account's email address (Editor access). You won't be able to write to it until he does this.

### 4. First run

The first time the skill writes a lead, your browser will open asking you to log into Google — log in with **your own account** and click Allow. After that, a `token.json` is saved in this folder and it won't ask again. Claude can trigger this run for you once steps 1-3 are done.

### 5. Use it

Just ask Claude Code, in plain language, for leads — e.g. "find me some leads" or "get me 5 more clinics in Glasgow." No fixed command syntax. See `SKILL.md` for exactly how it researches and qualifies each lead.

## What this does NOT need

- No Google Places API key
- No Gemini API key
- No Apify account/key
- No access to Logan's Discord bot, browser session, or any of his credentials

Every business is found and researched through Claude's own native web search/browsing, plus a free lookup on Companies House's public register (no key needed there either — it's a normal public website).
