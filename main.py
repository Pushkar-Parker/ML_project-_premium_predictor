import streamlit as st
from prediction import predict

# Set the title of the Streamlit app
st.title("Health Insurance Premium Calculator")

# Categories and their options
categories = {
    "Age": None,  # Numeric input

    "Gender": ['Male', 'Female'],

    "Region": ['Northwest', 'Southeast', 'Northeast', 'Southwest'],

    "Marital_status": ['Unmarried', 'Married'],

    "Number Of Dependants": None,  # Numeric input

    "BMI_Category": ['Normal', 'Obesity', 'Overweight', 'Underweight'],
    
    "Smoking_Status": ['No Smoking', 'Regular', 'Occasional'],
    
    "Employment_Status": ['Salaried', 'Self-Employed', 'Freelancer'],
    
    "Income_Lakhs": None,  # Numeric input
    
    "Medical History": [
        'Diabetes', 'High blood pressure', 'No Disease',
        'Diabetes & High blood pressure', 'Thyroid', 'Heart disease',
        'High blood pressure & Heart disease', 'Diabetes & Thyroid',
        'Diabetes & Heart disease'
    ],
    
    "Insurance_Plan": ['Bronze', 'Silver', 'Gold'],
    
    "Genetical_Risk": None  # Numeric input
}

# Numeric input parameters
numeric_parameters = {
    "Age": {"min_value": 18, "max_value": 100, "step": 1},
    
    "Number Of Dependants": {"min_value": 0, "max_value": 20, "step": 1},
    
    "Income_Lakhs": {"min_value": 1, "max_value": 200, "step": 1},
    
    "Genetical_Risk": {"min_value": 0, "max_value": 5, "step": 1}
}

# Adjustable parameter for layout: Number of columns per row
cols_per_row = 3

# Collect user inputs
user_inputs = {}
keys = list(categories.keys())
num_categories = len(keys)
rows = (num_categories + cols_per_row - 1) // cols_per_row

for i in range(rows):
    cols = st.columns(cols_per_row)
    for j in range(cols_per_row):
        index = i * cols_per_row + j
        if index < num_categories:
            category = keys[index]
            with cols[j]:
                if categories[category] is None:
                    params = numeric_parameters[category]
                    user_inputs[category] = st.number_input(
                        f"{category}", 
                        **params
                    )
                else:
                    user_inputs[category] = st.selectbox(category, categories[category])

# Add a Predict button
if st.button("Predict"):
    prediction = predict(user_inputs)  # Output dictionary to terminal
    st.success(f"Predicted Premium : ₹{round(prediction[0])}")