from flask import Flask, request, jsonify
import os
import requests
import json

app = Flask(__name__)

# Set environment variables for configuration
CONTAINER2_URL = os.environ.get('CONTAINER2_URL', 'http://container2-service:5001')
STORAGE_PATH = os.environ.get('STORAGE_PATH', '/saikat_PV_dir')

# Ensure storage directory exists
os.makedirs(STORAGE_PATH, exist_ok=True)

@app.route('/store-file', methods=['POST'])
def store_file():
    try:
        # Parse JSON input
        data = request.get_json()
        
        # Validate JSON input
        if 'file' not in data or not data['file']:
            return jsonify({
                "file": None,
                "error": "Invalid JSON input."
            }), 400
            
        if 'data' not in data:
            return jsonify({
                "file": data['file'],
                "error": "Invalid JSON input."
            }), 400
        
        # Create file path
        filepath = os.path.join(STORAGE_PATH, data['file'])
        
        # Write data to file
        try:
            with open(filepath, 'w') as f:
                f.write(data['data'])
            
            return jsonify({
                "file": data['file'],
                "message": "Success."
            })
        except Exception as e:
            print(f"Error writing to file: {e}")
            return jsonify({
                "file": data['file'],
                "error": f"Error while storing the file to the storage."
            }), 500
            
    except Exception as e:
        print(f"General error: {e}")
        return jsonify({
            "file": None,
            "error": "Invalid JSON input."
        }), 400

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Parse JSON input
        data = request.get_json()
        
        # Validate JSON input
        if 'file' not in data or not data['file']:
            return jsonify({
                "file": None,
                "error": "Invalid JSON input."
            }), 400
            
        if 'product' not in data:
            return jsonify({
                "file": data['file'],
                "error": "Invalid JSON input."
            }), 400
        
        # Check if file exists
        filepath = os.path.join(STORAGE_PATH, data['file'])
        if not os.path.exists(filepath):
            return jsonify({
                "file": data['file'],
                "error": "File not found."
            }), 404
        
        # Forward request to Container 2
        try:
            response = requests.post(
                f"{CONTAINER2_URL}/calculate-sum",
                json=data,
                timeout=10
            )
            
            # Return response from Container 2
            return response.json(), response.status_code
            
        except requests.RequestException as e:
            print(f"Error calling container 2: {e}")
            return jsonify({
                "file": data['file'],
                "error": "Error communicating with calculation service."
            }), 500
            
    except Exception as e:
        print(f"General error: {e}")
        return jsonify({
            "file": None,
            "error": "Invalid JSON input."
        }), 400

@app.route('/start', methods=['POST'])
def start():
    # This endpoint is just to test your service
    return jsonify({"status": "Service is running"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
#This is a comment
