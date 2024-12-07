import streamlit as st
import boto3
import pymysql
import pandas as pd
import os

# AWS S3 Configuration
S3_BUCKETS = {
    'positive': 'positive-tweets',
    'neutral': 'neutral-tweets',
    'negative': 'negative-tweets'
}

# AWS Session Setup
session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    aws_session_token=os.getenv('AWS_SESSION_TOKEN')
)

# S3 Client
s3_client = session.client('s3')

# RDS Database Configuration
DB_CONFIG = {
    'host': 'twitterdatabase.clq2628wi96r.us-east-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'superawesometeam',
    'database': 'twitterdatabase'
}

# Custom CSS for page styling
st.markdown("""
    <style>
    .stApp {
        background-color: #f7f7f7;
        font-family: 'Arial', sans-serif;
    }
    .stTitle {
        font-size: 32px;
        color: #1da1f2;
        font-weight: bold;
    }
    .stText {
        font-size: 18px;
        color: #555555;
    }
    .selectbox {
        background-color: #f0f8ff;
        border: 1px solid #1da1f2;
        padding: 10px;
    }
    .stButton {
        background-color: #1da1f2;
        color: white;
        border-radius: 8px;
    }
    .stButton:hover {
        background-color: #0d95e8;
    }
    </style>
""", unsafe_allow_html=True)

# Custom CSS for page styling
st.markdown("""
    <style>
    .blue-text {
        color: #1DA1F2;  /* Twitter Blue */
        font-size: 20px;  /* Adjust the font size here */
        font-weight: bold;
        text-align: left;  /* Center-align the text */
    }
    </style>
""", unsafe_allow_html=True)
def get_tweets_from_s3(sentiment: str) -> list:
    """Fetch tweet texts from S3 based on sentiment."""
    tweets = []
    bucket_name = S3_BUCKETS.get(sentiment)

    if not bucket_name:
        st.write("Invalid sentiment selected.")
        return tweets

    # List objects in the bucket
    response = s3_client.list_objects_v2(Bucket=bucket_name)

    if 'Contents' not in response:
        st.write("No objects found in this bucket.")
        return tweets

    # Fetch tweet texts from each file in the S3 bucket
    for obj in response['Contents']:
        tweet_key = obj['Key']
        file_response = s3_client.get_object(Bucket=bucket_name, Key=tweet_key)
        tweet_text = file_response['Body'].read().decode('utf-8')
        tweets.append(tweet_text)

    return tweets


def get_metadata_from_rds() -> pd.DataFrame:
    """Fetch tweet metadata (ID, USER, Date) from the RDS database."""
    connection = pymysql.connect(**DB_CONFIG)
    query = "SELECT ID, USER, Date FROM tweets_metadata;"
    df = pd.read_sql(query, connection)
    connection.close()
    return df


def display_tweets(tweets: list):
    """Display a list of tweets in the Streamlit app."""
    if tweets:
        for tweet_text in tweets:
            st.write(f"### Tweet:")
            st.write(f"{tweet_text}")
            st.write("---")
    else:
        st.write("No tweets found for the selected sentiment.")


def main():
    st.markdown('<h1 class="blue-text">Sentiment-Based Tweet Viewer</h1>', unsafe_allow_html=True)

    # Sentiment Selection
    sentiment = st.selectbox(
        "Select the type of Tweets you want to see!",
        ("positive", "neutral", "negative")
    )

    # Fetch tweets from S3
    st.write(f"Fetching {sentiment} tweets...")
    tweet_texts = get_tweets_from_s3(sentiment)

    # Display Tweets
    if tweet_texts:
        for tweet_text in tweet_texts:
            st.write(tweet_text)
            st.write("---")
    else:
        st.write("No tweets found for the selected sentiment.")

if __name__ == "__main__":
    main()