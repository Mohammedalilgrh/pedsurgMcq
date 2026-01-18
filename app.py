from flask import Flask, request, jsonify
import os
import logging

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Pediatric Surgery IQ Bot is running!"

@app.route('/health')
def health():
    return jsonify({"status": "ok", "message": "Bot is running"}), 200

@app.route('/webhook', methods=['POST'])
def webhook():
    # This is where Telegram webhook would go
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"🚀 Starting Flask server on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False)
