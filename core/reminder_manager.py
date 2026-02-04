from core.database import get_connection

# Conversation state
_waiting_for_reminder = False


def set_waiting(state: bool):
    global _waiting_for_reminder
    _waiting_for_reminder = state


def is_waiting():
    return _waiting_for_reminder


# Database-backed reminder functions
def add_reminder(text, time):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO reminders (text, remind_at) VALUES (?, ?)",
        (text, time)
    )
    conn.commit()
    conn.close()


def get_reminders():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT text, remind_at FROM reminders")
    rows = cursor.fetchall()
    conn.close()
    return rows
