from flask import Flask, jsonify, render_template
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    try:
        json_path = 'sinewave_data.json'
        if not os.path.exists(json_path):
            return jsonify({"error": "No data available"}), 404

        with open(json_path, 'r') as f:
            data = json.load(f)

        # Validate keys
        if 'sine' not in data or 'timestamp' not in data:
            return jsonify({"error": "Malformed data"}), 400

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use Render's port if available
    app.run(debug=True, host='0.0.0.0', port=port)
