from flask import Flask, render_template, request, jsonify
from nlp.intent_classifier import predict_intent
from core.reminder_manager import (
    add_reminder,
    get_reminders,
    set_waiting,
    is_waiting
)
from core.database import init_db
from core.scheduler import start_scheduler
from nlp.time_parser import parse_time

app = Flask(__name__)

# Initialize DB and scheduler AFTER app creation
init_db()
start_scheduler()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip().lower()

    # If assistant is waiting for reminder content
    if is_waiting():
        time = parse_time(user_message)

        if not time:
            set_waiting(False)  # 🔥 EXIT WAIT MODE
            return jsonify({
                "response": (
                    "I couldn't understand the time. "
                    "Please try again like: 'set a reminder tomorrow at 6pm'."
                )
            })

        add_reminder(user_message, time)
        set_waiting(False)

        return jsonify({
            "response": f"✅ Reminder set for {time}"
        })


    intent = predict_intent(user_message)

    if intent == "greeting":
        response = "Hello! How can I help you?"

    elif intent == "set_reminder":
        set_waiting(True)
        response = "What should I remind you about and when?"

    elif intent == "show_reminders":
        reminders = get_reminders()

        if not reminders:
            response = "You have no reminders yet."
        else:
            response = "📌 Your reminders:\n" + "\n".join(
                f"- {text} (at {time})"
                for text, time in reminders
            )

    elif intent == "help":
        response = (
            "I can:\n"
            "• Set reminders\n"
            "• Show reminders\n"
            "• Answer simple questions"
        )

    else:
        response = "Sorry, I didn’t understand that."

    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True)
