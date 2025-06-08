import streamlit as st
import requests
from datetime import datetime
import pandas as pd

def format_timestamp(timestamp_str):
    return datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S").strftime("%b %d, %Y %H:%M")

def main():
    st.set_page_config(page_title="AVM Conversational AI", layout="wide")
    
    # Custom CSS with fixed header and updated styling
    st.markdown("""
        <style>
            /* Reset default streamlit padding */
            .stApp {
                margin-top: 0;
                padding-top: 60px !important;
            }
            
            .header-container {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                z-index: 999999;
                background-color: white;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                padding: 10px 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .company-name {
               display: flex;
               align-items: center;
               gap: 5px;
            }

            .company-name-avm {
                color: #FF6B00; /* Bright orange color */
                font-size: 32px; /* Adjusted font size for 'AVM' */
                font-weight: bold;
            }

            .company-name-consulting {
                color: #1A2A49; /* Slightly darker navy blue */
                font-size: 32px; /* Adjusted font size for 'Consulting' to match 'AVM' */
                font-weight: normal;
                margin-top: 0.1cm; /* Minor adjustment to align vertically */
                display: inline-block;
            }
            .help-icon {
                cursor: pointer;
                font-size: 24px;
                color: #666;
                position: relative;
            }
            
            .help-content {
                display: none;
                position: absolute;
                right: 0;
                top: 100%;
                background: white;
                padding: 15px;
                border-radius: 5px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                width: 300px;
                z-index: 1001;
            }
            
            .help-icon:hover .help-content {
                display: block;
            }
            
            .footer {
                background-color: #f8f9fa;
                padding: 20px;
                text-align: center;
                color: #333;
                font-size: 14px;
                line-height: 1.6;
                margin-top: 40px;
                border-top: 1px solid #ddd;
                max-width: 1200px;
                margin-left: auto;
                margin-right: auto;
            }
        </style>
        
        <div class="header-container">
            <div class="company-name">
                <span class="company-name-avm">AVM</span>
                <span class="company-name-consulting">Consulting</span>
            </div>
            <div class="help-icon">
                <span>❔</span>
                <div class="help-content">
                    <h4>Quick Help Guide</h4>
                    <p>Welcome to AVM Consulting's AI Assistant!</p>
                    <ul>
                        <li>Type your query in the text area</li>
                        <li>Click 'Submit Query' to get a response</li>
                        <li>View your recent searches on the left panel</li>
                        <li>For support: info@avmconsulting.net</li>
                    </ul>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if 'query_history' not in st.session_state:
        st.session_state.query_history = []

    # Create columns with 25% and 75% width
    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader("Recent Searches")
        if st.session_state.query_history:
            for item in reversed(st.session_state.query_history):
                with st.expander(f"Query: {item['query'][:50]}..."):
                    st.text(f"Time: {format_timestamp(item['timestamp'])}")
                    st.markdown("**Response:**")
                    st.write(item['response'])
        else:
            st.info("No recent searches. Try submitting a query!")

    with col2:
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

    # Updated footer with new content
    st.markdown(
        """
        <div class="footer">
            <div>
                AVM Consulting is an AWS Advanced Partner and global consultancy headquartered in Reston VA specializing in DevSecOps, CloudOps, Observability, Data and Enterprise Architecture
            </div>
            <div style="margin-top: 10px; font-size: 12px; color: #666;">
                © 2024 AVM Consulting. All rights reserved. Contact us: info@avmconsulting.net
            </div>
        </div>
        """, unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
