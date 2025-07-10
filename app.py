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
    usage[user_ip][today] = today_count + 1
    save_usage(usage)

    return render_template('result.html', story=story, genre=genre)
