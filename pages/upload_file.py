import streamlit as st
from streamlit.logger import get_logger
import boto3
import time

# Set up logging for the app
LOGGER = get_logger(__name__)

# AWS S3 Configuration
AWS_REGION = "us-east-1"  # Replace with your AWS region
S3_BUCKET = "tweet-uploads"  # Your S3 bucket name

# Initialize S3 client
s3 = boto3.client('s3', region_name=AWS_REGION)

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

def upload_to_s3(content, bucket_name, file_key):
    """Uploads text content to S3 as a file."""
    try:
        s3.put_object(Bucket=bucket_name, Key=file_key, Body=content)
        LOGGER.info(f"Uploaded {file_key} to {bucket_name}")
        return f"https://{bucket_name}.s3.{AWS_REGION}.amazonaws.com/{file_key}"
    except Exception as e:
        LOGGER.error(f"Failed to upload {file_key}: {e}")
        raise e

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
            # Generate a unique file key for the tweet
            file_key = f"tweet_{int(time.time())}.txt"

            try:
                # Upload the tweet to S3
                s3_url = upload_to_s3(tweet, S3_BUCKET, file_key)
                st.success(f"Your tweet has been posted successfully!")
                st.write(f"View your tweet on S3: [Tweet File]({s3_url})")
            # except Exception:
                # st.error("Failed to upload tweet to S3. Please try again.")
        else:
            # Show error message if the tweet input is empty
            st.error("Please type something before posting.")

if __name__ == "__main__":
    main()