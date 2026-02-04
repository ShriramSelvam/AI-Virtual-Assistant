from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from core.database import get_connection

scheduler = BackgroundScheduler()

def check_reminders():
    conn = get_connection()
    cursor = conn.cursor()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        "SELECT id, text FROM reminders WHERE remind_at <= ?",
        (now,)
    )
    reminders = cursor.fetchall()

    for rid, text in reminders:
        print(f"🔔 REMINDER: {text}")
        cursor.execute("DELETE FROM reminders WHERE id = ?", (rid,))

    conn.commit()
    conn.close()

def start_scheduler():
    scheduler.add_job(check_reminders, "interval", seconds=30)
    scheduler.start()
