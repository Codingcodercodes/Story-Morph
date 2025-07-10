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
    today_count = usage.get(user_ip, {}).get(today, {}).get("count", 0)

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

    try:
        response = model.generate_content(prompt)
        story = response.text
    except Exception as e:
        if "Too Many Requests" in str(e):
            flash("The AI is taking a break 🧠💤 Too many requests. Please try again in a little while!")
        else:
            flash("Something went wrong. Try again later!")
        return redirect('/')

    # Update usage
    if user_ip not in usage:
        usage[user_ip] = {}

    usage[user_ip][today] = {
        "count": today_count + 1,
        "genre": genre
    }

    save_usage(usage)
    return render_template('result.html', story=story, genre=genre)

@app.route('/analytics')
def analytics():
    today = datetime.now().strftime("%Y-%m-%d")
    usage = load_usage()

    total_users = 0
    total_stories = 0
    genre_counts = defaultdict(int)

    for ip, dates in usage.items():
        if today in dates:
            total_users += 1
            total_stories += dates[today]['count']
            genre_counts[dates[today]['genre']] += 1

    return render_template(
        'analytics.html',
        total_users=total_users,
        total_stories=total_stories,
        genre_counts=genre_counts
    )


if __name__ == '__main__':
    app.run(debug=True)
