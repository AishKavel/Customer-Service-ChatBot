from flask import Flask, render_template, request, jsonify
from utils import generate_rag_response
from flask_cors import CORS
import time

app = Flask(__name__)

# Enable Cross-Origin Resource Sharing if needed for frontend-backend interaction
CORS(app)

@app.get("/")
def index_get():
    """
    Serve the main page of the application.
    """
    return render_template("index.html")

@app.post("/predict")
def predict():
    """
    Handle POST requests to the /predict endpoint to process user input
    and generate a response using the RAG model.
    """
    try:
        # Extract message from the request
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({'error': 'Invalid input: "message" field is required.'}), 400

        text = data.get("message", "").strip()
        if not text:
            return jsonify({'error': 'Invalid input: "message" cannot be empty.'}), 400

        # Generate response using RAG
        start_time = time.time()
        response = generate_rag_response(text)
        end_time = time.time()

        print(f"Took {end_time - start_time} seconds total")

        # Format response
        # response = {
        #     'input': text,
        #     'output': answer,
        #     'response_time': round(end_time - start_time, 2)
        # }
        #print(response)

        return jsonify(response)

    except Exception as e:
        # Log error details for debugging purposes
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred while processing the request.'}), 500

if __name__ == "__main__":
    # Run the application in debug mode for easier development and debugging
    app.run(debug=True)
