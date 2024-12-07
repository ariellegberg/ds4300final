import streamlit as st
import boto3
import pymysql
import pandas as pd
import os
import io
# AWS S3 Configuration
S3_BUCKETS = {
    'positive': 'positive-tweets',
    'neutral': 'neutral-tweets',
    'negative': 'negative-tweets'
}

# AWS session setup
session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    aws_session_token=os.getenv('AWS_SESSION_TOKEN')
)

# Create S3 client using the session
s3_client = session.client('s3')

# RDS Database Configuration
DB_HOST = 'twitterdatabase.clq2628wi96r.us-east-1.rds.amazonaws.com'
DB_USER = 'admin'
DB_PASSWORD = 'superawesometeam'
DB_NAME = 'twitterdatabase'


def get_tweets_from_s3(sentiment):
    """Fetch tweet texts from S3 based on sentiment."""
    tweets = []
    bucket_name = S3_BUCKETS[sentiment]

    # List objects in the bucket
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    st.write("Response:", response)  # Print the full response

    if 'Contents' not in response:
        st.write("No objects found in this bucket.")
        return tweets

    # Iterate through all objects in the bucket and fetch their text content
    for obj in response['Contents']:
        tweet_key = obj['Key']

        # Fetch the object from S3 using its key
        file_response = s3_client.get_object(Bucket=bucket_name, Key=tweet_key)

        # Read the text content from the file
        tweet_text = file_response['Body'].read().decode('utf-8')
        tweets.append(tweet_text)

    return tweets


def get_metadata_from_rds():
    """Fetch tweet metadata from the RDS database."""
    connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    query = "SELECT ID, USER, Date FROM tweets_metadata;"
    df = pd.read_sql(query, connection)
    connection.close()
    return df

def main():
    st.title("Sentiment-Based Tweet Viewer")

    # Sentiment Selection
    sentiment = st.selectbox(
        "Select the type of tweets to display:",
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

