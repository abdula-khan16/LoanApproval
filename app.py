import os
import pickle
import numpy as np
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Load the model
try:
    with open('logistic_regression_model.pkl', 'rb') as f:
        model = pickle.load(f)
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model could not be loaded.'}), 500

    try:
        data = request.json
        
        # 1. Parse the known form inputs
        # Note: We provide default 0 if something is missing
        age = float(data.get('age', 0))
        annual_income = float(data.get('annualIncome', 0))
        loan_amount = float(data.get('loanAmount', 0))
        loan_term = float(data.get('loanTerm', 0))
        credit_score = float(data.get('creditScore', 0))
        employment_years = float(data.get('employmentYears', 0))
        
        # Categorical handling (Mock mapping)
        property_area_map = {'Urban': 0, 'Semiurban': 1, 'Rural': 2}
        property_val = property_area_map.get(data.get('propertyArea', 'Urban'), 0)
        
        education_val = 1 if data.get('education') == 'Graduate' else 0
        self_employed_val = 1 if data.get('selfEmployed') == 'Yes' else 0
        dependents = float(data.get('dependents', 0))

        # 2. The model specifically requires exactly 45 features based on inspection.
        # Since we don't have the original exact feature mappings/encoder, we'll map 
        # the inputs we collected to the first 10 columns, and pad the remaining 35 with zeros.
        # This will ensure the code runs successfully and provides an example for you 
        # to correctly substitute the mapped indices later.
        
        features = np.zeros((1, 45))
        features[0, 0] = age
        features[0, 1] = annual_income
        features[0, 2] = loan_amount
        features[0, 3] = loan_term
        features[0, 4] = credit_score
        features[0, 5] = employment_years
        features[0, 6] = property_val
        features[0, 7] = education_val
        features[0, 8] = self_employed_val
        features[0, 9] = dependents
        
        # 3. Make prediction
        prediction = model.predict(features)
        
        # Convert prediction result to a human-readable response
        # Usually 1 = Approved, 0 = Rejected for typical Loan models
        result_text = "Approved" if prediction[0] == 1 else "Rejected"
        
        return jsonify({'status': 'success', 'prediction': result_text})

    except Exception as e:
        print("Prediction Error:", e)
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
