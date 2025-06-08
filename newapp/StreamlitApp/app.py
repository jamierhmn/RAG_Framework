# frontend.py
import streamlit as st
import requests
from datetime import datetime
import pandas as pd

def format_timestamp(timestamp_str):
    return datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S").strftime("%b %d, %Y %H:%M")

def main():
    st.set_page_config(page_title="AVM Conversational AI", layout="wide")
    
    if 'query_history' not in st.session_state:
        st.session_state.query_history = []

    st.title("📚 AVM Conversational AI")
    st.markdown("---")

    # Create two columns
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Submit Query")
        with st.form("query_form"):
            input_data = st.text_area("Enter your query:", height=100)
            submit_button = st.form_submit_button("Submit Query")

        if submit_button and input_data:
            try:
                with st.spinner("Processing query..."):
                    response = requests.post(
                        "http://localhost:8000/query",
                        json={"query": input_data}
                    )
                
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.query_history = data['history']
                    
                    st.success("Query processed successfully!")
                    st.markdown("### Response:")
                    st.write(data['response'])
                else:
                    st.error(f"Error: {response.status_code}")
            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {str(e)}")

    with col2:
        st.subheader("Recent Searches")
        if st.session_state.query_history:
            for item in reversed(st.session_state.query_history):
                with st.expander(f"Query: {item['query'][:50]}..."):
                    st.text(f"Time: {format_timestamp(item['timestamp'])}")
                    st.markdown("**Response:**")
                    st.write(item['response'])
        else:
            st.info("No recent searches. Try submitting a query!")

if __name__ == "__main__":
    main()
