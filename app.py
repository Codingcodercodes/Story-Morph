from flask import Flask, render_template, request, redirect, flash
from datetime import datetime
from collections import defaultdict
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Structure: { ip_address: { "date": "2025-07-10", "count": 1 } }
user_usage = defaultdict(lambda: {"date": "", "count": 0})



# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Any random string works for now


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    user_ip = request.remote_addr
    today = datetime.now().strftime("%Y-%m-%d")

    usage = user_usage[user_ip]

    if usage["date"] != today:
        # First visit today – reset count
        usage["date"] = today
        usage["count"] = 0

    if usage["count"] >= 2:
        flash("You've already generated 2 stories today! Come back tomorrow 😉✌️")
        return redirect('/')

    user_input = request.form['real_moment'].strip()
    genre = request.form['genre']

    if not user_input:
        flash("Please share a moment before generating a story!")
        return redirect('/')

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
    usage["count"] += 1  # Increment usage

    return render_template('result.html', story=story, genre=genre)



if __name__ == '__main__':
    app.run(debug=True)
