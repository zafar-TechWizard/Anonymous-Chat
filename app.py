from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)
MESSAGES_FILE = 'messages.json'  # Path to the JSON file

# Initialize messages file if it doesn't exist
if not os.path.exists(MESSAGES_FILE):
    with open(MESSAGES_FILE, 'w') as f:
        json.dump([], f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    sender = request.form['sender']
    recipient = request.form['recipient']
    content = request.form['content']

    # Read existing messages
    with open(MESSAGES_FILE, 'r') as f:
        messages = json.load(f)

    # Add new message
    messages.append({
        'sender': sender,
        'recipient': recipient,
        'content': content
    })

    # Write updated messages back to file
    with open(MESSAGES_FILE, 'w') as f:
        json.dump(messages, f, indent=4)

    return jsonify({"status": "Message sent"})

@app.route('/get_messages', methods=['GET'])
def get_messages():
    recipient = request.args.get('recipient')

    # Read existing messages
    with open(MESSAGES_FILE, 'r') as f:
        messages = json.load(f)

    # Filter messages by recipient
    recipient_messages = [msg for msg in messages if msg['recipient'] == recipient]

    return jsonify(recipient_messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
