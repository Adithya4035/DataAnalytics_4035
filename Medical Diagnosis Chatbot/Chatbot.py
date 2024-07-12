import logging
import os
from dotenv import load_dotenv
from flask import Flask, render_template, session, request, jsonify
from flask_session import Session
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.DEBUG)  # Set logging level to DEBUG
logger = logging.getLogger(__name__)

# Initialize Flask app with custom template folder
app = Flask(__name__, template_folder='D:/Project')

# Configuring server-side session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Load and preprocess the CSV file
data = pd.read_csv("D:/Project/Disease_symptom_and_patient_profile_dataset.csv")

# Standardize gender labels
data['Gender'] = data['Gender'].str.lower()

# Preprocess the data
le_gender = LabelEncoder()
le_gender.fit(['male', 'female'])  # Ensure encoder knows both 'male' and 'female'
data['Gender'] = le_gender.transform(data['Gender'])

le_disease = LabelEncoder()
data['Disease'] = le_disease.fit_transform(data['Disease'])

X = data[['Age', 'Gender', 'Fever', 'Cough', 'Fatigue', 'Blood Pressure', 'Outcome Variable']]
y = data['Disease']

# Define the preprocessing pipeline for categorical features
categorical_features = ['Fever', 'Cough', 'Fatigue', 'Blood Pressure', 'Outcome Variable']
categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Define the preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', categorical_transformer, categorical_features)
    ],
    remainder='passthrough'  # To include the rest of the columns
)

# Define the pipeline with the preprocessor and the model
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier())
])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
pipeline.fit(X_train, y_train)

# Save the trained model and encoders
joblib.dump(pipeline, 'model.pkl')
joblib.dump(le_gender, 'le_gender.pkl')
joblib.dump(le_disease, 'le_disease.pkl')

@app.route("/")
def root_route():
    return render_template("template.html")

@app.route("/send_message", methods=['POST'])
def send_message():
    try:
        user_message = request.json['message'].strip().lower()
        
        if 'state' not in session:
            session['state'] = 'age'
            session['symptoms'] = {'Fever': 'No', 'Cough': 'No', 'Fatigue': 'No', 'Blood Pressure': 'Normal', 'Outcome Variable': 'No'}
            return jsonify({"message": "Welcome to the medical diagnosis chatbot. Please enter your age:"})
        
        if session['state'] == 'age':
            try:
                age = int(user_message)
                session['age'] = age
                session['state'] = 'gender'
                return jsonify({"message": "Thank you. Now, please enter your gender:"})
            except ValueError:
                return jsonify({"message": "Please enter a valid age as a number:"})
        
        elif session['state'] == 'gender':
            gender = user_message.lower()
            if gender not in ['male', 'female']:
                return jsonify({"message": "Please enter a valid gender: 'male' or 'female'."})
            session['gender'] = gender
            session['state'] = 'symptoms'
            return jsonify({"message": "Thank you. Now, please describe your symptoms (e.g., 'fever, cough, headache'):"})
        
        elif session['state'] == 'symptoms':
            session['symptoms'] = update_symptoms(session['symptoms'], user_message)
            response = generate_response(session['age'], session['gender'], session['symptoms'])
            if 'disease' in session:
                return jsonify({"message": response + " If you have any more symptoms, please describe them or type 'done' if you are finished."})
            else:
                return jsonify({"message": response + " Please provide more symptoms or type 'done' if you are finished."})
        
        elif session['state'] == 'complete':
            if user_message == 'done':
                reset_session()
                return jsonify({"message": "Thank you for using our medical diagnosis chatbot. If you have any more questions or concerns, please consult a healthcare professional. To start a new diagnosis, please enter your age:"})
            else:
                session['symptoms'] = update_symptoms(session['symptoms'], user_message)
                response = generate_response(session['age'], session['gender'], session['symptoms'])
                return jsonify({"message": response + " Please provide more symptoms or type 'done' if you are finished."})
    
    except Exception as e:
        logger.error(f"Error processing user message: {e}")
        return jsonify({"message": f"An error occurred: {e}. Please try again."})

def update_symptoms(symptoms_dict, symptoms):
    symptoms_list = symptoms.lower().split(',')
    for symptom in symptoms_list:
        symptom = symptom.strip()
        if symptom in symptoms_dict:
            symptoms_dict[symptom] = 'Yes'
    return symptoms_dict

def generate_response(age, gender, symptoms):
    try:
        # Load the trained model and label encoders
        model = joblib.load('model.pkl')
        le_gender = joblib.load('le_gender.pkl')
        le_disease = joblib.load('le_disease.pkl')
        
        # Preprocess the input
        gender_encoded = le_gender.transform([gender])[0]
        input_data = pd.DataFrame([[age, gender_encoded, 
                                    symptoms['Fever'], 
                                    symptoms['Cough'], 
                                    symptoms['Fatigue'], 
                                    symptoms['Blood Pressure'], 
                                    symptoms['Outcome Variable']]], 
                                  columns=['Age', 'Gender', 'Fever', 'Cough', 'Fatigue', 'Blood Pressure', 'Outcome Variable'])
        
        # Predict the disease
        prediction = model.predict(input_data)
        disease = le_disease.inverse_transform(prediction)[0]
        
        session['disease'] = disease
        session['state'] = 'complete'
        response = f"Based on your age, gender, and symptoms, you might be experiencing {disease}."
        
        return response
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return f"An error occurred while generating the response: {e}. Please try again."

def reset_session():
    session.pop('age', None)
    session.pop('gender', None)
    session.pop('symptoms', None)
    session.pop('state', None)
    session.pop('disease', None)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
