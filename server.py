from flask import Flask, request, jsonify, render_template
from serpapi import GoogleSearch   

app = Flask(__name__)
API_KEY = "894807be90e816940e80a2259a46174f3dd1ff55ed27cab5bbc6665592fc0e82"
memory = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/ask")
def ask():
    query = request.args.get("q", "").strip().lower()

    greetings = ["Hi! 😊", "Hello! 👋", "Hey there!"]
    intros = [
        "I'm RashankAI, created by Rashank Singh in 2025!",
        "Well! I'm RashankAI — built by Rashank Singh to help you!"
    ]
    hardcoded = {
        "hi": greetings[0],
        "hello": greetings[1],
        "who are you": intros[0],
        "what is your name": intros[1],
        "who created you": "Oh! That would be Rashank Singh in 2025. 🧠",
        "when were you created": "Well! I was created in the exciting year of 2025.",
        "what is the meaning of life": "Ah, the big one! Maybe it's love, growth, and kindness 💫.",
        "why are we here": "To connect, grow, and explore! 🌍"
    }

    if not query:
        return jsonify({"error": "Empty question."})

    if query in memory:
        return jsonify({"answer": f"You’ve asked that before 😄: {memory[query]}"})

    if query in hardcoded:
        answer = hardcoded[query]
        memory[query] = answer
        return jsonify({"answer": answer})

    try:
        search = GoogleSearch({
            "q": query,
            "api_key": API_KEY,
            "num": 1
        })
        result = search.get_dict()
        answer = "Sorry, I couldn’t find a solid answer."

        if "answer_box" in result:
            answer = result["answer_box"].get("answer") or result["answer_box"].get("snippet") or answer
        elif "organic_results" in result and len(result["organic_results"]) > 0:
            answer = result["organic_results"][0].get("snippet", answer)

        memory[query] = answer
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
