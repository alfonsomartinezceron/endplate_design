import streamlit as st
import pandas as pd
import joblib

# Load model pipeline
@st.cache_resource
def load_model():
    return joblib.load("endplate_model.pkl")

model = load_model()

# Streamlit UI
st.title("🚧 Endplate Design Criteria Predictor")
st.write("Upload an Excel file with new endplate design data to predict if designs are acceptable.")

# File uploader
uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file:
    # Read Excel
    new_data = pd.read_excel(uploaded_file)
    new_data = new_data.drop(columns =['symmetry','item'])
    new_data['collapse'] = new_data['collapse'].replace({1: 'yes', 0: 'no'})
    
    st.subheader("📂 Uploaded Data Preview")
    st.dataframe(new_data.head())

    # Make predictions
    preds = model.predict(new_data)

    # Add predictions to dataframe
    new_data["Predicted_Design_Criteria"] = preds
    new_data["Status"] = ["✅ Acceptable" if p < 1 else "❌ Not Acceptable" for p in preds]

    st.subheader("🔮 Predictions")

    st.dataframe(new_data)



