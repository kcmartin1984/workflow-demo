import json
import os

# Default quota warning threshold (percentage)
QUOTA_WARNING_THRESHOLD = 80  

def load_data():
    """Load sample_data.json. If missing or invalid, return fallback data."""
    try:
        with open("src/sample_data.json", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️ sample_data.json not found, using fallback data")
        return {
            "meetings": 0,
            "chats": 0,
            "onedrive": {"viewed": 0, "edited": 0, "shared": 0},
            "quota": {"used": 0, "limit": 100}
        }
    except json.JSONDecodeError:
        print("⚠️ sample_data.json invalid format, using fallback data")
        return {
            "meetings": 0,
            "chats": 0,
            "onedrive": {"viewed": 0, "edited": 0, "shared": 0},
            "quota": {"used": 0, "limit": 100}
        }

def generate_report(data):
    """Print weekly report summary."""
    print("=== Weekly Report ===")
    print(f"Meetings: {data.get('meetings', 'No data')}")
    print(f"Chats: {data.get('chats', 'No data')}")
    onedrive = data.get("onedrive", {})
    print(f"OneDrive Viewed: {onedrive.get('viewed', 'No data')}")
    print(f"OneDrive Edited: {onedrive.get('edited', 'No data')}")
    print(f"OneDrive Shared: {onedrive.get('shared', 'No data')}")

def check_quota(data):
    """Check quota usage and print warning if threshold exceeded."""
    quota = data.get("quota", {})
    used = quota.get("used", 0)
    limit = quota.get("limit", 100)
    pct = (used / limit) * 100 if limit > 0 else 0

    print("\n=== Quota Monitoring ===")
    print(f"Used: {used}/{limit} ({pct:.1f}%)")

    if pct >= QUOTA_WARNING_THRESHOLD:
        print("⚠️ Warning: Quota usage exceeded threshold! Consider scaling or cleanup.")
    else:
        print("✅ Quota usage within safe range.")

def main():
    # Allow overriding threshold via environment variable
    threshold = os.getenv("QUOTA_THRESHOLD_PERCENT")
    if threshold and threshold.isdigit():
        global QUOTA_WARNING_THRESHOLD
        QUOTA_WARNING_THRESHOLD = int(threshold)

    data = load_data()
    generate_report(data)
    check_quota(data)

if __name__ == "__main__":
    main()
