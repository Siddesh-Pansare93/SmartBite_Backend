from flask import Flask, request, jsonify
from diet import generate_diet
from scan_packed_food import scan
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Route to handle requests from the Node.js backend
@app.route('/plan_diet', methods=['POST'])
def plan_diet():
    print("Received request to plan diet")
    try:
        # Parse JSON data from the request
        user_profile_data = request.json
        if not user_profile_data:
            return jsonify({"error": "Invalid or missing JSON data"}), 400
        
        print("User Profile Data:", user_profile_data)

        # Pass the data to the generate function
        result = generate_diet(user_profile_data)

        # Return the result as a JSON response
        print("Result:", result)
        return jsonify(result), 200

    except Exception as e:
        # Handle errors and return a 500 status
        print("Error:", e)
        return jsonify({"error": str(e)}), 500
from flask import Flask, request, jsonify
import os
import json
from scan_packed_food import scan

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)




@app.route('/scan_img', methods=['POST'])
def scan_img():
    print("Received request to scan image")
    try:
        # Log incoming request data for debugging
        print("Request Files:", request.files)
        print("Request Form:", request.form)

        # Check if an image file is included in the request
        if 'image' not in request.files:
            print("Error: No image file provided")
            return jsonify({"error": "No image file provided"}), 400

        # Get the uploaded image file
        image_file = request.files['image']

        # Validate the file type
        if not image_file.filename.endswith(('.png', '.jpg', '.jpeg')):
            print("Error: Invalid file type. Only PNG, JPG, and JPEG are allowed.")
            return jsonify({"error": "Invalid file type. Only PNG, JPG, and JPEG are allowed."}), 400

        # Save the file to the uploads folder
        file_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
        image_file.save(file_path)

        # Retrieve and validate the description
        description = request.form.get("description")
        if not description:
            print("Error: No description provided")
            return jsonify({"error": "No description provided"}), 400

        # Retrieve and parse user_Details
        user_details = request.form.get("user_Details")
        if not user_details:
            print("Error: No user_Details provided")
            return jsonify({"error": "No user_Details provided"}), 400
        user_details = json.loads(user_details)  # Convert JSON string to dictionary

        # Retrieve and parse user_Diet
        user_diet = request.form.get("user_Diet")
        if not user_diet:
            print("Error: No user_Diet provided")
            return jsonify({"error": "No user_Diet provided"}), 400
        user_diet = json.loads(user_diet)  # Convert JSON string to dictionary

        # Log received data
        print("Description:", description)
        print("User Details:", user_details)
        print("User Diet:", user_diet)

        # Call the scan function with the received data
        result = scan(file_path, description, user_details, user_diet)

        print(result)

        # Return the result
        return jsonify(result), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)