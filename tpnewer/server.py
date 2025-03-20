from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot import chatbot_response  # Ensure correct import

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_input = data.get("message", "")
        if not user_input:
            return jsonify({"response": "❌ No message received."})

        response = chatbot_response(user_input)  # Ensure chatbot returns a string
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"response": f"❌ Server error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
