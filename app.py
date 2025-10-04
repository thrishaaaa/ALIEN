# python-chatbot/app.py
import ollama
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    # Get the incoming message from the Java backend
    user_message = request.json.get('message', '')

    # --- This is your Prompt Engineering ---
    prompt = f"""
    You are an expert U.S. visa assistant. Respond ONLY with a valid JSON object.
    Do not include any text outside of the JSON structure.

    The JSON object must have these keys:
    - "main_reply": A conversational answer to the user's question.
    - "actionable_items": A list of key steps or documents. If none, provide an empty list.
    - "disclaimer": Always include the string: "This is for informational purposes only. Consult official sources."

    User's question: "{user_message}"

    Your JSON response:
    """

    response = ollama.chat(
        model='llama3', 
        messages=[{'role': 'user', 'content': prompt}],
        options={'temperature': 0}
    )

    bot_reply_json_string = response['message']['content']

    try:
        # Parse the JSON string from the model's response
        structured_response = json.loads(bot_reply_json_string)
        return jsonify(structured_response)
    except json.JSONDecodeError:
        # Provide a fallback if the model returns invalid JSON
        return jsonify({
            "main_reply": "I apologize, but I couldn't structure the response correctly. Please try rephrasing your question.",
            "actionable_items": [],
            "disclaimer": "An error occurred."
        })

if __name__ == '__main__':
    # Run the server on port 5001
    app.run(host='0.0.0.0', port=5001)