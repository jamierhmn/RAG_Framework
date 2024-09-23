# app.py
import streamlit as st
import requests

# Streamlit UI for querying the RAG pipeline
st.title("RAG Pipeline Query Interface")

# Input box for user query
query = st.text_input("Enter your query:")

if st.button('Send Query'):
    if query:
        try:
            # Send query to the Flask API
            response = requests.post('http://localhost:5000/query', json={"query": query})
            if response.status_code == 200:
                response_data = response.json()
                st.success("Response from the RAG pipeline:")
                st.write(response_data['response'])
            else:
                st.error("Error fetching response from server")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a query")

