import streamlit as st

# Path to the Twitter logo PNG (replace with the correct path)
logo_path = 'logo.png'

def set_page_style():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #F0F4F8;
        }
        h1, h2 {
            font-family: 'Arial', sans-serif;
            color: #007BFF;
        }
        .stButton>button {
            background-color: #007BFF;
            color: white;
            font-size: 16px;
            font-weight: bold;
            border-radius: 8px;
        }
        .stButton>button:hover {
            background-color: #0056b3;
        }
        </style>
        """, unsafe_allow_html=True
    )

# Set the page style
set_page_style()

def main():
    # Display the Twitter Logo
    st.image(logo_path, width=100)  # You can adjust the width as needed

    # Main Section
    st.title("Arielle and Ella's DS4300 Final Project")
    st.write("Welcome to the sentiment-based Tweet viewer! Please enter your Twitter username below to upload and view tweets.")

    # User Input for Twitter Username
    tik_tok_username = st.text_input('Enter Your Twitter Username', key='tik_tok', placeholder='e.g. @username')

    # Upload Button for Tweet
    upload = st.button('Upload Tweet')

    if upload:
        if tik_tok_username:
            # Redirect to file upload page when clicked
            st.switch_page('pages/upload_file.py')
        else:
            st.error("Please enter a valid Twitter username.")

if __name__ == "__main__":
    main()
