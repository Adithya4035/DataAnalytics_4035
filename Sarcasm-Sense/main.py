# main.py

import logging
from flask import Flask, request, jsonify, render_template
from waitress import serve
import joblib
from routes import create_app

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load trained model and TF-IDF vectorizer
try:
    model = joblib.load('models/sarcasm_detector_model.pkl')
    tfidf = joblib.load('models/tfidf_vectorizer.pkl')
    logger.info("Model and vectorizer loaded successfully.")
except Exception as e:
    logger.error(f"Error loading model or vectorizer: {e}")
    raise

# Create the Flask application using the create_app function
app = create_app(model, tfidf)

# Define route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Define route for the results page
@app.route('/result')
def result():
    return render_template('result.html')

# Define route for predicting sarcasm scores
@app.route('/predict', methods=['POST'])
def predict_sarcasm():
    try:
        data = request.get_json()
        comment = data.get('comment', '')

        if not comment:
            return jsonify({'error': 'Comment not provided'}), 400

        # Preprocess new comment using TF-IDF vectorizer
        X_new = tfidf.transform([comment])

        # Predict sarcasm score
        sarcasm_score = model.predict_proba(X_new)[:, 1][0]  # Ensure correct index

        # Generate sarcastic comment based on sarcasm score
        sarcastic_comment = get_sarcastic_comment(sarcasm_score)  # Define this function accordingly

        return jsonify({'score': float(sarcasm_score), 'comment': sarcastic_comment})
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        return jsonify({'error': 'Internal server error'}), 500

# Entry point for running the application
if __name__ == "__main__":
    try:
        # Run the Flask app using Waitress
        serve(app, host='localhost', port=8080)
    except Exception as e:
        logger.error(f"Error starting the server: {e}")
        raise
