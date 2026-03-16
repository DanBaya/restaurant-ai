from flask import Flask, render_template, request, jsonify
from main import ask_question
from database import init_db, save_message, get_history
import time

app = Flask(__name__)

# retry db connection on startup
for i in range(10):
    try:
        init_db()
        print("Database connected.")
        break
    except Exception as e:
        print(f"Waiting for database... ({i+1}/10)")
        time.sleep(3)

@app.route("/")
def index():
    history = get_history()
    return render_template("index.html", history=history)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    answer = ask_question(question)
    save_message(question, answer)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)