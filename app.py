import streamlit as st
import pandas as pd
import openai
import plotly.express as px
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key (loaded from the .env file)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Custom CSS styling
st.markdown("""
<style>
.stButton>button {
    background-color: #4CAF50;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# Add a logo and title
st.image(r'C:\Users\user\Pictures\download.jpg', width=200)
st.title("Delv AI-like Web App")

# Sidebar for file upload
st.sidebar.header("Upload Your Dataset")
uploaded_file = st.sidebar.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    try:
        # Read the dataset
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)

        # Display dataset preview
        st.write("### Dataset Preview")
        st.dataframe(df)

        # Show basic dataset statistics
        st.write("### Summary Statistics")
        st.write(df.describe())

        # AI Query Section
        st.write("### Ask Questions About Your Data")
        query = st.text_input("Enter your question:")

        if query:
            try:
                # Convert dataset to string for AI input
                dataset_summary = df.head(5).to_string()
                prompt = f"Here is a sample of the dataset:\n{dataset_summary}\n\nQuestion: {query}\nAnswer:"

                # Use OpenAI GPT model to answer
                with st.spinner('Waiting for AI response...'):
                    response = openai.Completion.create(
                        engine="text-davinci-003",
                        prompt=prompt,
                        max_tokens=150
                    )
                st.write("### AI Response")
                st.write(response.choices[0].text.strip())
            except Exception as e:
                st.error(f"Error with AI response: {e}")

        # Visualization Section
        st.write("### Create Visualizations")
        chart_type = st.selectbox("Select Chart Type", ["Scatter Plot", "Line Chart", "Bar Chart"])
        x_axis = st.selectbox("Select X-Axis", df.columns)
        y_axis = st.selectbox("Select Y-Axis", df.columns)

        if st.button("Generate Chart"):
            try:
                if chart_type == "Scatter Plot":
                    fig = px.scatter(df, x=x_axis, y=y_axis, title="Scatter Plot")
                elif chart_type == "Line Chart":
                    fig = px.line(df, x=x_axis, y=y_axis, title="Line Chart")
                elif chart_type == "Bar Chart":
                    fig = px.bar(df, x=x_axis, y=y_axis, title="Bar Chart")
                st.plotly_chart(fig)
            except Exception as e:
                st.error(f"Error generating chart: {e}")
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
else:
    st.write("Please upload a dataset to get started.")

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("**Contact Us:** info@yourcompany.com")
