from datetime import datetime, timedelta
import re
from dateutil import parser

def parse_time(text):
    text = text.lower()
    now = datetime.now()

    # --- Handle "tomorrow at X" ---
    tomorrow_match = re.search(r"tomorrow at (\d{1,2})(?::(\d{2}))?\s*(am|pm)", text)
    if tomorrow_match:
        hour = int(tomorrow_match.group(1))
        minute = int(tomorrow_match.group(2) or 0)
        meridian = tomorrow_match.group(3)

        if meridian == "pm" and hour != 12:
            hour += 12
        if meridian == "am" and hour == 12:
            hour = 0

        dt = (now + timedelta(days=1)).replace(
            hour=hour, minute=minute, second=0, microsecond=0
        )
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    # --- Fallback: try dateutil on shorter phrase ---
    try:
        dt = parser.parse(text, fuzzy=True, default=now)
        if dt > now:
            return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        pass

    return None
