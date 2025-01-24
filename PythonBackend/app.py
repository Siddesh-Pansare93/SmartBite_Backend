from flask import Flask, request, jsonify
from diet import generate_diet


app = Flask(__name__)


# Route to handle requests from the Node.js backend
@app.route('/plan_diet', methods=['POST'])
def plan_diet():
    try:
        print("Received request to plan diet")
        # Parse JSON data from the request
        user_profile_data = request.json
        if not user_profile_data:
            return jsonify({"error": "Invalid or missing JSON data"}), 400

        # Pass the data to the generate function
        result = generate_diet(user_profile_data)

        # Return the result as a JSON response
        print("Result:", result)
        print(type(result[0]))
        return jsonify(result), 200

    except Exception as e:
        # Handle errors and return a 500 status
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)