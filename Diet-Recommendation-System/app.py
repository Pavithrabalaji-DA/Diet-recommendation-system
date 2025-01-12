import streamlit as st
import pandas as pd
import pickle
from sklearn.cluster import KMeans
import time  # Used to simulate a delay for loading spinner

# Loading the model
filename = "dietrec.sav"
loaded_model = pickle.load(open(filename, 'rb'))

# Reading Food.csv for diet recommendation
data = pd.read_csv("food.csv")
diet = data.drop("Food_items", axis=1)

# Applying k-means and defining the number of clusters
km = KMeans(n_clusters=4)
y_predicted = km.fit_predict(diet)

# Adding a new column containing the cluster a food item is part of
data['cluster'] = y_predicted

# Streamlit app settings
st.set_page_config(page_title="Diet Recommendation System", page_icon="diet.ico", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        body {
            background-color: #f5f5f5;
            font-family: 'Arial', sans-serif;
        }
        .header {
            background-color: #FF9F00;
            padding: 20px;
            color: white;
            text-align: center;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .title {
            font-size: 2.5em;
            font-family: 'Verdana', sans-serif;
            font-weight: bold;
        }
        .subtitle {
            font-size: 1.5em;
            font-family: 'Arial', sans-serif;
            color: #616161;
            margin-top: -10px;
        }
        .card {
            background-color: white;
            padding: 20px;
            margin: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .stButton button {
            background-color: #FF6600;
            color: white;
            border-radius: 15px;
            padding: 15px 35px;
            font-size: 18px;
            font-weight: bold;
            transition: transform 0.3s ease, background-color 0.3s ease;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .stButton button:hover {
            background-color: #cc5200;
            transform: scale(1.1);
        }
        .stButton button:active {
            transform: scale(1.05);
        }
        .footer {
            position: fixed;
            bottom: 10px;
            left: 0;
            width: 100%;
            text-align: center;
            padding: 15px;
            background-color: #2c3e50;
            color: white;
            font-size: 1.2em;
            font-weight: bold;
        }
        .tips {
            background-color: #e0f7fa;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .table {
            font-size: 16px;
            text-align: center;
        }
        /* Overlapping buttons */
        .overlap-container {
            position: relative;
            display: inline-block;
        }
        .button1 {
            position: absolute;
            left: 0;
            z-index: 1;
        }
        .button2 {
            position: absolute;
            left: 120px;
            z-index: 1;
        }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
    <div class="header">
        <span class="title">Diet Recommendation System 🍎🥗</span>
        <div class="subtitle">Personalized recommendations based on your BMI and health data.</div>
    </div>
""", unsafe_allow_html=True)

# Interactive Sliders for weight and height
col1, col2 = st.columns(2)
with col1:
    weight = st.slider("Select your weight in kg ⚖️", min_value=30.0, max_value=200.0, value=70.0, step=0.1)
with col2:
    height = st.slider("Select your height in m 📏", min_value=1.2, max_value=2.5, value=1.7, step=0.01)

# Check for zero height and display error
if height == 0:
    st.error("Error: Height should be a non-zero value. 🚫")
else:
    # Calculate BMI
    bmi = weight / (height ** 2)

    # Predict using the model
    Xdata = {'Height': [height], 'Weight': [weight], 'BMI': [bmi]}
    df = pd.DataFrame(Xdata, columns=['Height', 'Weight', 'BMI'])
    predicted = loaded_model.predict(df)
    predicted_cluster = predicted[0]

    # Displaying BMI and diet recommendation with enhanced styling
    st.markdown(f"### Your BMI is **{bmi:.2f}** 🏷️", unsafe_allow_html=True)

    st.markdown("### **Diet Recommendations 🍽️** based on your BMI and weight:")

    # Create a table for food recommendations with Quantity
    recommended_food = data[data['cluster'] == predicted_cluster].sample(5)
    recommended_food['Quantity'] = ['1 serving' for _ in range(len(recommended_food))]  # Sample quantity

    # Displaying food recommendations in a table format
    st.markdown(f"<div class='card'>", unsafe_allow_html=True)
    st.write(recommended_food[['Food_items', 'Quantity']].style.set_properties(**{
        'text-align': 'center',
        'font-family': 'Arial, sans-serif',
        'font-size': '14px'
    }))
    st.markdown(f"</div>", unsafe_allow_html=True)

# Loading spinner
with st.spinner('Processing... please wait! 🕒'):
    time.sleep(2)  # Simulating a delay

# Create creative buttons with custom actions
col3, col4 = st.columns(2)
with col3:
    st.markdown('<div class="overlap-container">', unsafe_allow_html=True)
    if st.button('Get More Recommendations 🌟', key='more_recommendations', use_container_width=True):
        st.success('Here are more diet tips coming your way! 🌈')
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="overlap-container">', unsafe_allow_html=True)
    if st.button('Calculate Again 🔄', key='calculate_again', use_container_width=True):
        st.success('Your BMI has been recalculated! 💪')
    st.markdown('</div>', unsafe_allow_html=True)

# Dynamic Feedback (Custom interactive buttons)
if st.button("Try a Different Diet Plan 🍽️"):
    st.balloons()  # Show balloons animation
    st.success("You’re ready to explore new diet plans! 🎉")

if st.button("Clear All Inputs 🧹"):
    st.session_state.clear()  # Clear all inputs

# Add a section for healthy tips with emojis
st.markdown("""
    <div class="tips">
        <h3 style="color: #1e88e5;">Healthy Eating Tips 🍎:</h3>
        <ul>
            <li>Drink plenty of water 💧 daily.</li>
            <li>Include a variety of fruits 🍓 and vegetables 🥕 in your diet.</li>
            <li>Limit processed foods 🍟 and sugary beverages 🧃.</li>
            <li>Maintain a balance ⚖️ between protein, fats, and carbohydrates.</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

# Footer Section with bold thank you message
st.markdown("""
    <div class="footer">
        <strong>Thank you for visiting this project! 👩‍💻</strong>
        <strong> Created by pavithra B</strong>
    </div>
""", unsafe_allow_html=True)

# Hide deprecation warnings
st.set_option('deprecation.showfileUploaderEncoding', False)
