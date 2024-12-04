import pandas as pd
import boto3
import sqlalchemy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# Define Sentiment Labeling Function
def get_sentiment_label(text, analyzer):
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']
    if compound >= 0.05:
        return 'positive'
    elif compound <= -0.05:
        return 'negative'
    else:
        return 'neutral'


# AWS S3 and RDS Configuration
AWS_REGION = "your-region"  # e.g., "us-east-1"
S3_BUCKETS = {
    "positive": "your-positive-bucket",
    "neutral": "your-neutral-bucket",
    "negative": "your-negative-bucket",
    "nonprocessed": "your-nonprocessed-bucket",
}
RDS_CONFIG = {
    "host": "your-rds-endpoint",
    "port": 3306,
    "user": "your-username",
    "password": "your-password",
    "database": "your-database",
}

# Initialize AWS Clients
s3_client = boto3.client('s3', region_name=AWS_REGION)
analyzer = SentimentIntensityAnalyzer()


# Function to Upload to S3
def upload_to_s3(bucket_name, file_key, content):
    s3_client.put_object(Bucket=bucket_name, Key=file_key, Body=content)
    print(f"Uploaded to {bucket_name}: {file_key}")


# Main Function
def process_tweets_to_s3_and_rds(csv_file):
    # Read CSV
    df = pd.read_csv(csv_file)

    # Initialize Connection to RDS
    engine = sqlalchemy.create_engine(
        f"mysql+pymysql://{RDS_CONFIG['user']}:{RDS_CONFIG['password']}@"
        f"{RDS_CONFIG['host']}:{RDS_CONFIG['port']}/{RDS_CONFIG['database']}"
    )

    # Process Each Tweet
    for _, row in df.iterrows():
        # Extract Text and Metadata
        text = row['Text']
        metadata = row.drop(['Text']).to_dict()

        # Determine Sentiment
        sentiment = get_sentiment_label(text, analyzer)
        metadata['Sentiment'] = sentiment

        # Upload Text to Appropriate S3 Bucket
        file_key = f"{metadata['Id']}.txt" if 'Id' in metadata else f"{_}.txt"
        upload_to_s3(S3_BUCKETS[sentiment], file_key, text)

        # Upload Metadata to RDS
        pd.DataFrame([metadata]).to_sql(
            'tweets_metadata', engine, index=False, if_exists='append'
        )


# Call the Function
if __name__ == "__main__":
    process_tweets_to_s3_and_rds('tweets.csv')
