import pandas as pd
from joblib import load

model_rest = load(r"D:\software\notebooks\Supervised_learning\practice\codebasics\health_project\app\artifacts\model_rest.joblib")
model_young = load(r"D:\software\notebooks\Supervised_learning\practice\codebasics\health_project\app\artifacts\model_young.joblib")

scaler_rest = load(r"D:\software\notebooks\Supervised_learning\practice\codebasics\health_project\app\artifacts\scaler_rest.joblib")
scaler_young = load(r"D:\software\notebooks\Supervised_learning\practice\codebasics\health_project\app\artifacts\scaler_young.joblib")

def preprocess_input(user_input):
    expected_columns = [
    'Age',
    'Number Of Dependants',
    'Income_Lakhs',
    'Insurance_Plan',
    'Genetical_Risk',
    'normalised_score',
    'Gender_Male',
    'Region_Northwest',
    'Region_Southeast',
    'Region_Southwest',
    'Marital_status_Unmarried',
    'BMI_Category_Obesity',
    'BMI_Category_Overweight',
    'BMI_Category_Underweight',
    'Smoking_Status_Occasional',
    'Smoking_Status_Regular',
    'Employment_Status_Salaried',
    'Employment_Status_Self-Employed'
    ] ### column names can be exported to a file then imported

    df = pd.DataFrame(0, columns=expected_columns, index = [0])

    # print(type(user_input['Region']), type(user_input['Age']))
    for x, y in user_input.items():
        if isinstance(user_input[x], int):
            df[x] = y
              
        if isinstance(user_input[x], str):
            if x == 'Gender':
                if y == 'Male':
                    df['Gender_Male'] = 1
            
            if x == 'Region': 
                if y == 'Northwest':
                    df['Region_Northwest'] = 1
     
                elif y == 'Southeast':
                    df['Region_Southeast'] = 1
     
                elif y == 'Southwest':
                    df['Region_Southwest'] = 1

            if x == 'Marital_status':
                if y == 'Unmarried':
                    df['Marital_status_Unmarried'] = 1

            if x == 'BMI_Category':
                if y == 'Obesity':
                    df['BMI_Category_Obesity'] = 1
                elif y == 'Overweight':
                    df['BMI_Category_Overweight'] = 1
                elif y == 'Underweight':
                    df['BMI_Category_Underweight'] = 1

            if x == 'Smoking_Status':
                if y == 'Occasional':
                    df['Smoking_Status_Occasional'] = 1
                elif y == 'Regular':
                    df['Smoking_Status_Regular'] = 1

            if x == 'Employment_Status':
                if y == 'Salaried':
                    df['Employment_Status_Salaried'] = 1
                elif y == 'Self-Employed':
                    df['Employment_Status_Self-Employed'] = 1

            if x == 'Insurance_Plan':
                if y == 'Bronze':
                    df['Insurance_Plan'] = 1
                elif y == 'Silver':
                    df['Insurance_Plan'] = 2
                elif y == 'Gold':
                    df['Insurance_Plan'] = 3

            if x == 'Medical History':
                df['normalised_score'] = calculate_normalized_score(y, 0, 14)

    scaled_df = scaling_data(df)

    return scaled_df

def scaling_data(df):
    if df["Age"][0] <= 25:
        scaler_object = scaler_young
    else:
        scaler_object = scaler_rest

    cols_to_scale = scaler_object['cols_to_scale']
    scaler = scaler_object['scaler']
    df['Income_Level'] = None

    df[cols_to_scale] = scaler.transform(df[cols_to_scale])
    df = df.drop('Income_Level', axis = 1)
    
    return df

def calculate_normalized_score(medical_history, min_score, max_score):
    # Define risk scores
    risk_scores = {
        'diabetes': 6,
        'heart disease': 8,
        'high blood pressure': 6,
        'thyroid': 5,
        'no disease': 0,
        'none': 0,
        'None': 0
    }

    # Convert the medical history to lowercase and split by ' & '
    diseases = [disease.strip() for disease in medical_history.lower().split('&')]

    # Map risk scores and sum them up
    total_risk_score = sum(risk_scores.get(disease, 0) for disease in diseases)

    # Normalize the total risk score
    normalized_score = (total_risk_score - min_score) / (max_score - min_score) if max_score > min_score else 0

    return normalized_score

def predict(user_input):
    df = preprocess_input(user_input)

    if user_input["Age"] <= 25:
        prediction = model_young.predict(df)

        return prediction
    else:
        prediction = model_rest.predict(df)

        return prediction