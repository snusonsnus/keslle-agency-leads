---
name: yazke-lead-finder
description: Use when Yazke asks (in plain language) for new sales leads, more leads, or to find businesses to call — no fixed command syntax required.
---

# Yazke's Lead Finder

Finds real, fully-contactable local businesses and writes them into the shared "Agency Leads" Google Sheet. Runs entirely on native web browsing/search — no Google Places key, no Gemini key, no Apify key, no dependency on Logan's Discord bot or his other project. The only script involved is `sheet_writer.py` in this folder, which only writes rows — it never decides what counts as a good lead. That judgment happens here, in this skill.

## Who to target

**Never target tech companies.** In this priority order — everything before trades:

1. Clinics — aesthetics, dental, physio, chiropractic, veterinary
2. Law firms / professional services — solicitors, accountants
3. Personal care & fitness — hair salons, beauty salons, personal trainers/gyms
4. Driving instructors
5. Counselling / therapy practices
6. Real estate — estate & letting agents
7. Trades — **last resort only**, and only these four: roofers, plumbers, electricians, heating engineers

Ask Yazke which category and which town/area if he hasn't said, rather than guessing.

## Batch size

Default to **5** leads on a first request for a new category/area, even if he asks for more — validate quality with him before scaling up. Once a category+area has proven good, later batches can be bigger if he asks.

## Per-business research process

Work through candidates using parallel subagents (a few at a time — 3-5 concurrent, not the whole batch at once; too many simultaneous automated look-ups at once can look like bot traffic to the sites being checked). Before researching a candidate, run `python sheet_writer.py list-names` and skip any business already in the sheet.

For each candidate, in this order:

1. **Website check — first, always.** Does the business have a real, working website? If not, stop here. Skip this lead entirely, don't research further.
2. **Contact info.** Check the business's own website (its contact/about page) first — often gives phone and email in one visit. If either is still missing, check its Google Business Profile and Facebook page next. A business can have more than one phone number (e.g. landline + mobile, main line + emergency/out-of-hours) — capture all of them, comma-separated.
3. **Owner name.** Search the business name on Companies House's public register: `https://find-and-update.company-information.service.gov.uk/search?q=<business name>`. Open the matching company's officers / people-with-significant-control page and read the real name(s) listed — this is public data, no API key needed. If Companies House gives a clear match, that name is confirmed, use it as-is. If nothing matches there, fall back to whatever real name turns up in general web research (the business's own About page, press mentions, Google Business Profile) and write it with a trailing `?` (e.g. `Jane Smith?`) to mark it as unconfirmed rather than hiding it.
4. **Judge the lead, don't just fill fields.** Even with all 4 fields technically present, drop a business that looks clearly defunct, inactive, or fake (dead site, no real reviews or signals of activity, obviously abandoned listing) — the goal is a real, currently-operating business, not just a filled row.

## The hard rule

**All 4 fields — website, owner name, email, phone number(s) — must be genuinely found, or the lead is dropped. No partial rows, ever.** A missing website skips it immediately (step 1); a missing owner/email/phone after full research also skips it. Never write a guess into any field, and never leave one blank.

## Writing a passing lead

Call `sheet_writer.py` once per passing lead:

```
python sheet_writer.py add --name "<business name>" --category "<the category it matched>" --website "<url>" --owner "<name or name?>" --email "<email>" --phones "<one or more, comma-separated>"
```

## Reporting back

After a batch, tell Yazke plainly: how many leads were found and added, how many candidates were skipped and why (no website / no owner / no contact info / judged not a real active business), and the sheet link.
