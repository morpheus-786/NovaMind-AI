# Import Libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import openai
from dotenv import load_dotenv
import os
import sqlite3
import streamlit_authenticator as stauth

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize SQLite Database
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY, task TEXT, input TEXT, output TEXT)')
conn.commit()

# Streamlit Configuration
st.set_page_config(page_title="Delv AI", layout="wide", page_icon="🌟")

# Authentication
names = ["John Doe", "Jane Smith"]
usernames = ["johndoe", "janesmith"]
passwords = ["123", "456"]  # Replace with hashed passwords
cookie_expiry_days=30

# Create Streamlit Authenticator
authenticator = stauth.Authenticate(
    names, usernames, passwords, "app_home", "random_key", 
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    st.sidebar.success(f"Welcome {name}!")

    # Navigation
    st.sidebar.title("Navigation")
    task = st.sidebar.radio("Select a Task", ["Summarization", "Data Visualization", "History"])

    # Summarization Feature
    if task == "Summarization":
        st.header("Summarize Text or File")
        choice = st.radio("Input Type", ["Text", "Upload File"])

        user_input = ""
        if choice == "Text":
            user_input = st.text_area("Enter text to summarize")
        elif choice == "Upload File":
            uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
            if uploaded_file:
                user_input = uploaded_file.read().decode("utf-8")

        if st.button("Summarize"):
            if user_input:
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=f"Summarize this: {user_input}",
                    max_tokens=150
                )
                summary = response.choices[0].text.strip()
                st.success(summary)

                # Save to Database
                if st.button("Save Result"):
                    cursor.execute("INSERT INTO history (task, input, output) VALUES (?, ?, ?)", ("Summarization", user_input, summary))
                    conn.commit()
                    st.success("Result saved to database!")
            else:
                st.warning("No input provided.")

    # Data Visualization Feature
    elif task == "Data Visualization":
        st.header("Data Visualization")
        uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.write("Preview of Data:", df.head())

            chart_type = st.selectbox("Select Chart Type", ["Line", "Bar", "Scatter", "Pie"])
            x_axis = st.selectbox("Choose X-axis", df.columns)
            y_axis = st.selectbox("Choose Y-axis", df.columns)

            if chart_type == "Line":
                chart = px.line(df, x=x_axis, y=y_axis)
            elif chart_type == "Bar":
                chart = px.bar(df, x=x_axis, y=y_axis)
            elif chart_type == "Scatter":
                chart = px.scatter(df, x=x_axis, y=y_axis)
            elif chart_type == "Pie":
                chart = px.pie(df, names=x_axis, values=y_axis)

            st.plotly_chart(chart)

    # History Feature
    elif task == "History":
        st.header("Saved Results")
        cursor.execute("SELECT * FROM history")
        rows = cursor.fetchall()

        if rows:
            for row in rows:
                st.subheader(f"Task: {row[1]}")
                st.write(f"Input: {row[2]}")
                st.write(f"Output: {row[3]}")
        else:
            st.write("No history found.")

else:
    st.sidebar.error("Invalid credentials")