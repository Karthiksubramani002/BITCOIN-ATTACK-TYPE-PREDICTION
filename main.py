import streamlit as st
import pandas as pd
import pickle

# Load the trained model
with open("voting.pkl", "rb") as f:
    model = pickle.load(f)

# Streamlit app
st.title("Bitcoin Ransomware Attack Prediction")
st.write("Predict the likelihood of ransomware attacks based on input features.")

# Sidebar for user inputs
st.sidebar.header("Input Features")
def user_inputs():
    year = st.sidebar.number_input("Year:", value=2024, min_value=2000, max_value=2100, step=1)
    day = st.sidebar.number_input("Day of the Year:", value=1, min_value=1, max_value=365, step=1)
    length = st.sidebar.number_input("Transaction Length (bytes):", value=0.0, step=0.1)
    weight = st.sidebar.number_input("Transaction Weight:", value=0.0, step=0.1)
    count = st.sidebar.number_input("Input/Output Count:", value=0, step=1)
    looped = st.sidebar.selectbox("Looped Transaction (Yes=1, No=0):", options=[0, 1])
    neighbors = st.sidebar.number_input("Neighbor Transactions:", value=0, step=1)
    income = st.sidebar.number_input("Transaction Income:", value=0.0, step=0.01)

    data = {
        "year": year,
        "day": day,
        "length": length,
        "weight": weight,
        "count": count,
        "looped": looped,
        "neighbors": neighbors,
        "income": income,
    }
    return pd.DataFrame([data])

input_df = user_inputs()

# Display user inputs
st.subheader("User Input Features")
st.write(input_df)

# Prediction button
if st.button("Predict"):
    try:
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0]

        st.subheader("Prediction Result")
        if prediction == 1:
            st.error(f"The transaction is likely **suspicious**. (Probability: {probability[1]:.2f})")
        else:
            st.success(f"The transaction is likely **normal**. (Probability: {probability[0]:.2f})")
    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")

# Additional information
st.sidebar.markdown("### About the Model")
st.sidebar.write("This model predicts whether a Bitcoin transaction is linked to ransomware activity based on the input features.")
