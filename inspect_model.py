import pickle

try:
    with open('logistic_regression_model.pkl', 'rb') as f:
        model = pickle.load(f)
        print("Model Type:", type(model))
        
        # Check if the model has feature_names_in_ attribute (scikit-learn 1.0+)
        if hasattr(model, 'feature_names_in_'):
            print("Features:", list(model.feature_names_in_))
        else:
            print("No feature_names_in_ attribute found.")
            
        print("Model coefficients (if linear):")
        if hasattr(model, 'coef_'):
            print("Coef shape:", model.coef_.shape)
            
except Exception as e:
    print("Error loading or inspecting model:", e)
