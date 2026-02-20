from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def receive_webhook():
    data = request.json or request.form.to_dict()
    
    print(f"\n[{datetime.now()}] Webhook received!")
    print(json.dumps(data, indent=2))
    
    # Handle incident updates
    if 'incident' in data:
        incident = data['incident']
        print(f"INCIDENT: {incident['name']} — Status: {incident['status']}")
    
    # Handle component updates
    if 'component' in data:
        component = data['component']
        print(f"COMPONENT: {component['name']} — Status: {component['status']}")

    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)