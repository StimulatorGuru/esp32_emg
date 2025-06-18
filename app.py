from flask import Flask, jsonify, render_template, request
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

        if 'sine' not in data or 'timestamp' not in data:
            return jsonify({"error": "Malformed data"}), 400

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ NEW: Accept sinewave data from MATLAB
@app.route('/upload', methods=['POST'])
def upload():
    try:
        data = request.get_json()
        if 'sine' not in data or 'timestamp' not in data:
            return jsonify({"error": "Invalid data format"}), 400

        with open('sinewave_data.json', 'w') as f:
            json.dump(data, f)

        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Use dynamic port and 0.0.0.0 for Render
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
