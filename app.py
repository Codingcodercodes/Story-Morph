from flask import Flask, render_template, request, redirect, flash
from datetime import datetime
from collections import defaultdict
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)
app.secret_key = "supersecretkey"

USAGE_FILE = "/tmp/usage.json"

# Load user usage from JSON file
def load_usage():
    try:
        with open(USAGE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save user usage back to JSON file
def save_usage(usage_data):
    with open(USAGE_FILE, "w") as f:
        json.dump(usage_data, f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    user_ip = request.remote_addr
    today = datetime.now().strftime("%Y-%m-%d")
    usage = load_usage()

    # Get today's count or default to 0
    today_count = usage.get(user_ip, {}).get(today, 0)

    if today_count >= 2:
        flash("You've already generated 2 stories today! Come back tomorrow 🌙")
        return redirect('/')

    user_input = request.form['real_moment']
    genre = request.form['genre']

    prompt = f"""
    Turn this real-life moment into a creative {genre} short story:
    "{user_input}"

    The story should be:
    - 3 to 5 paragraphs long
    - Written in a storytelling tone
    - Have a beginning, twist, and ending
    - Be immersive, but loosely based on the original event
    """

    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content(prompt)
    story = response.text

    # Update usage
    if user_ip not in usage:
        usage[user_ip] = {}
    usage[user_ip][today] = today_count + 1
    save_usage(usage)

    return render_template('result.html', story=story, genre=genre)

if __name__ == '__main__':
    app.run(debug=True)
