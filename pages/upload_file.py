import streamlit as st
from streamlit.logger import get_logger
from pathlib import Path
import os

# Set up logging for the app
LOGGER = get_logger(__name__)

def set_page_style():
    """Function to set custom styles for the Streamlit page."""
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #F0F4F8;
        }
        h1, h2, h3 {
            font-family: 'Arial', sans-serif;
            color: #007BFF;
        }
        .stButton>button {
            background-color: #007BFF;
            color: white;
            font-size: 16px;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px 20px;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #0056b3;
        }
        .stTextInput>div>input {
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
        }
        </style>
        """, unsafe_allow_html=True
    )

def main():
    """Main function to render Streamlit app."""
    # Set custom page styles
    set_page_style()

    # Title Section
    st.title("Tweet Something!")
    st.write("## Please Upload Your Tweet Below")

    # Input for the Tweet text
    tweet = st.text_input("What's on your mind?", placeholder="Enter your tweet here...")

    # Submit Button
    submit = st.button('Post Your Tweet!')

    if submit:
        if tweet:
            # You can add your tweet handling logic here
            st.success(f"Your tweet: '{tweet}' has been posted!")
            # For now, let's simulate the transition to another page
            st.write("Redirecting to Twitter Feed...")
            st.switch_page('pages/twitter_feed.py')
        else:
            # Show error message if the tweet input is empty
            st.error("Please type something before posting.")

if __name__ == "__main__":
    main()
