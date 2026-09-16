# ==============================================================
#  SHEET WRITER — the only thing in this repo that touches Google.
#  No dependency on Logan's lead-finder project at all.
#
#  First run opens a browser for YOU to log into YOUR OWN Google
#  account (not Logan's) and click Allow. After that, a local
#  token.json is saved next to this script and it won't ask again.
#
#  Needs oauth_credentials.json next to this script -- see README.md
#  for how to get your own, free, in about 5 minutes.
# ==============================================================

import argparse
import os
import sys
from datetime import date

OAUTH_FILE = os.path.join(os.path.dirname(__file__), "oauth_credentials.json")
TOKEN_FILE = os.path.join(os.path.dirname(__file__), "token.json")
SHEET_NAME = "Agency Leads"
TAB_NAME   = "Leads"
HEADERS    = [
    "Business Name", "Category", "Website", "Owner Name",
    "Email", "Phone Number(s)", "Date Added", "Status", "Call Notes",
]

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def _get_creds():
    if not os.path.exists(OAUTH_FILE):
        print(
            f"ERROR: oauth_credentials.json not found at {OAUTH_FILE}\n"
            "See README.md — you need your own free Google OAuth client."
        )
        sys.exit(1)

    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request

    creds = None
    if os.path.exists(TOKEN_FILE):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        except Exception:
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None

        if not creds:
            print("\nOpening browser for Google login — log in with YOUR OWN account and click Allow...")
            flow = InstalledAppFlow.from_client_secrets_file(OAUTH_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
        print("Login successful. Token saved — won't ask again.\n")

    return creds


def _get_worksheet():
    import gspread

    creds = _get_creds()
    client = gspread.authorize(creds)

    try:
        spreadsheet = client.open(SHEET_NAME)
    except Exception as e:
        print(
            f"ERROR: Could not open a sheet named \"{SHEET_NAME}\".\n"
            "Make sure Logan has shared it with the Google account you just logged in with."
        )
        sys.exit(1)

    try:
        return spreadsheet.worksheet(TAB_NAME)
    except gspread.WorksheetNotFound:
        ws = spreadsheet.add_worksheet(title=TAB_NAME, rows=1000, cols=len(HEADERS))
        ws.update(values=[HEADERS], range_name="A1")
        ws.freeze(rows=1)
        return ws


def list_existing_business_names() -> list[str]:
    """Prints every business name already in the sheet, one per line --
    call this before researching a batch so already-researched businesses
    aren't researched (or written) twice."""
    ws = _get_worksheet()
    names = ws.col_values(1)[1:]  # skip header row
    return [n for n in names if n.strip()]


def append_lead(name: str, category: str, website: str, owner: str, email: str, phones: str) -> None:
    """Appends one real, fully-researched lead. All of name/website/owner/
    email/phones must already be non-empty -- this script does not decide
    what counts as a good lead, the skill's own research judgment does
    that before ever calling this."""
    for field_name, value in [
        ("name", name), ("website", website), ("owner", owner),
        ("email", email), ("phones", phones),
    ]:
        if not value.strip():
            print(f"ERROR: refusing to write a lead with an empty '{field_name}' field.")
            sys.exit(1)

    ws = _get_worksheet()
    ws.append_row([
        name, category, website, owner, email, phones,
        date.today().isoformat(), "",
    ])
    print(f"Added: {name}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Write to the shared Agency Leads sheet.")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list-names", help="Print every business name already in the sheet, one per line.")

    add = sub.add_parser("add", help="Append one fully-researched lead.")
    add.add_argument("--name", required=True)
    add.add_argument("--category", required=True)
    add.add_argument("--website", required=True)
    add.add_argument("--owner", required=True, help="Real name, or 'Name?' if not Companies-House-confirmed.")
    add.add_argument("--email", required=True)
    add.add_argument("--phones", required=True, help="One or more numbers, comma-separated.")

    args = parser.parse_args()

    if args.command == "list-names":
        for n in list_existing_business_names():
            print(n)
    elif args.command == "add":
        append_lead(args.name, args.category, args.website, args.owner, args.email, args.phones)

    return 0


if __name__ == "__main__":
    sys.exit(main())
