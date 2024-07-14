# routes.py

from flask import Flask, request, jsonify, render_template
from models import SarcasmDetector
import logging

def create_app(model=None, tfidf=None):
    app = Flask(__name__, static_folder='static')
    
    # Initialize logger
    app.logger.setLevel(logging.INFO)

    if model and tfidf:
        detector = SarcasmDetector(model=model, vectorizer=tfidf)
    else:
        app.logger.error("Model or vectorizer not provided.")
        detector = None

    def get_image_based_on_score(score):
        # Placeholder function to return image path based on sarcasm score
        # Customize this function as needed
        if score > 0.7:
            return 'static/images/high_sarcasm.png'
        elif score > 0.4:
            return 'static/images/medium_sarcasm.png'
        else:
            return 'static/images/low_sarcasm.png'

    @app.route("/")
    def home_route():
        return render_template("home.html")

    @app.route("/result")
    def result_route():
        sarcasm_score = request.args.get('score', 0.0, type=float)
        image_path = get_image_based_on_score(sarcasm_score)
        return render_template("result.html", score=sarcasm_score, image_path=image_path)

    @app.route("/analyze", methods=['POST'])
    def analyze_sarcasm():
        try:
            data = request.json
            comment = data.get('comment')
            if not comment:
                app.logger.error("Comment not provided.")
                return jsonify({'error': 'Comment not provided'}), 400
            
            if detector:
                sarcasm_score = detector.calculate_sarcasm_score(comment)
                return jsonify({'score': sarcasm_score})
            else:
                app.logger.error("Sarcasm detector not initialized.")
                return jsonify({'error': 'Sarcasm detector not initialized'}), 500

        except Exception as e:
            app.logger.error(f"Error during prediction: {e}")
            return jsonify({'error': 'Internal server error'}), 500

    return app
