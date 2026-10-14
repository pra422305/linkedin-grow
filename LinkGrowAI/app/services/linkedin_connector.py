import os
from datetime import date

import requests


class LinkedInConnectorError(RuntimeError):
    pass


def connection_status(profile_url):
    token = os.getenv("LINKEDIN_ACCESS_TOKEN", "").strip()
    return {
        "profile_url": profile_url,
        "has_profile_url": bool(profile_url),
        "has_access_token": bool(token),
        "ready": bool(profile_url and token),
        "message": (
            "Ready for authorized LinkedIn API sync."
            if profile_url and token
            else "Add a LinkedIn profile URL and configure LINKEDIN_ACCESS_TOKEN for authorized API sync."
        ),
    }


def fetch_authorized_metrics(profile_url):
    """Integration-ready connector.

    LinkedIn does not expose private impressions/profile analytics from a public profile URL alone.
    A production app must complete OAuth and call approved LinkedIn APIs for the authenticated user.
    """
    token = os.getenv("LINKEDIN_ACCESS_TOKEN", "").strip()
    if not profile_url:
        raise LinkedInConnectorError("Save your LinkedIn profile URL before syncing.")
    if not token:
        raise LinkedInConnectorError(
            "LinkedIn sync is not configured. Add an authorized LINKEDIN_ACCESS_TOKEN or use manual/CSV analytics import."
        )

    api_version = os.getenv("LINKEDIN_API_VERSION", "202610")
    headers = {
        "Authorization": f"Bearer {token}",
        "LinkedIn-Version": api_version,
        "X-Restli-Protocol-Version": "2.0.0",
    }
    response = requests.get("https://api.linkedin.com/v2/userinfo", headers=headers, timeout=15)
    if response.status_code >= 400:
        raise LinkedInConnectorError(f"LinkedIn authorization check failed with status {response.status_code}.")

    # A real deployment would next fetch the authenticated member's posts/URNs and approved analytics.
    # We return no fabricated rows because project rules require genuine observed metrics.
    return {
        "synced_on": date.today().isoformat(),
        "profile_url": profile_url,
        "records": [],
        "note": "Authorization works, but no post analytics endpoint is configured for this app yet.",
    }
