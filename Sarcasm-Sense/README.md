# Sarcasm Detector
This project implements a sarcasm detection system using machine learning and integrates it into a web application using Flask. Users can input text, and the system predicts the likelihood of sarcasm in the text.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [File Structure](#file-structure)
- [Contributing](#contributing)

## Overview
The Sarcasm Detector project leverages a logistic regression model trained on a dataset of Reddit comments. It preprocesses text data using TF-IDF vectorization and predicts sarcasm scores for user inputs. The backend is implemented in Python using Flask, and the frontend uses HTML, CSS, and JavaScript with Chart.js for visualization.

## Features
- **Sarcasm Detection**: Predicts sarcasm scores for user-provided text inputs.
- **Interactive UI**: Displays sarcasm scores dynamically using Chart.js and changes images based on the predicted score.
- **Training and Evaluation**: Includes functionality to train the sarcasm detection model and evaluate its performance.
- **Persistence**: Saves trained models and vectorizers for reuse.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/sarcasm-detector.git
   cd sarcasm-detector
   ```

2. Set up a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Train the model (if necessary):
   ```bash
   python models.py
   ```

2. Run the Flask application:
   ```bash
   python main.py
   ```

3. Open your web browser and go to `http://localhost:8080` to use the application.

## Technologies Used

- Python
- Flask
- scikit-learn
- pandas
- HTML/CSS/JavaScript
- Chart.js
- Waitress (for serving the Flask app)

## File Structure

```
sarcasm-detector/
│
├── main.py         # Flask application entry point
├── routes.py       # Defines Flask routes for web application
├── models.py       # Implements SarcasmDetector class for model training and prediction
├── static/         # Contains static assets (CSS, images)
│   ├── css/
│   │   └── styles.css
│   └── images/     # Images used for displaying sarcasm levels
├── templates/      # HTML templates for Flask application
│   ├── home.html
│   └── result.html
├── requirements.txt
└── README.md       # You are here!
```
##Sample Output

![image](https://github.com/user-attachments/assets/63a6d331-a362-4d3f-8376-18d8b762a0d1)

![image](https://github.com/user-attachments/assets/1410501d-931a-4644-ba2f-babe11233b82)


## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your suggested improvements.


