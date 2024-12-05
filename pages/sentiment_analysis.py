import pandas as pd
import boto3
import sqlalchemy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
from sqlalchemy.sql import text as sqltext

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
AWS_REGION = "us-east-1"
S3_BUCKETS = {
   "positive": "positive-tweets",
   "neutral": "neutral-tweets",
   "negative": "negative-tweets",
   "nonprocessed": "tweet-uploads",
}
RDS_CONFIG = {
   "host": "twitterdatabase.clq2628wi96r.us-east-1.rds.amazonaws.com",
   "port": 3306,
   "user": "admin",
   "password": "superawesometeam",
   "database": "twitterdatabase",
}

# Initialize AWS Clients
s3_client = boto3.client('s3', region_name=AWS_REGION)
try:
    response = s3_client.list_buckets()
    print("S3 Buckets:", response['Buckets'])
except Exception as e:
    print("Error accessing S3:", e)
analyzer = SentimentIntensityAnalyzer()

# Function to Upload to S3
def upload_to_s3(bucket_name, file_key, content):
   print('bucket', bucket_name)
   try:
       s3_client.put_object(Bucket=bucket_name, Key=file_key, Body=content)
       print(f"Uploaded to {bucket_name}: {file_key}")
   except Exception as e:
       print(f"Error uploading to S3: {e}")

def process_tweets_to_s3_and_rds(csv_file, interval=10):
   processed_ids = set()  # To track processed tweets

   # Direct connection to RDS
   engine = create_engine(
       f"mysql+pymysql://{RDS_CONFIG['user']}:{RDS_CONFIG['password']}@{RDS_CONFIG['host']}:{RDS_CONFIG['port']}/{RDS_CONFIG['database']}"
   )
   print("Database connection established")

   while True:
       # Read CSV
       df = pd.read_csv(csv_file, encoding='latin1')

       # Process Each New Tweet
       for _, row in df.iterrows():
           if row['ID'] in processed_ids:
               continue  # Skip already processed tweets

           # Extract Text and Metadata
           text = row['Text']
           metadata = row.drop(['Text']).to_dict()

           # Determine Sentiment
           sentiment = get_sentiment_label(text, analyzer)
           metadata['Sentiment'] = sentiment

           # Upload Text to Appropriate S3 Bucket
           file_key = f"{metadata['ID']}.txt" if 'ID' in metadata else f"{_}.txt"
           upload_to_s3(S3_BUCKETS[sentiment], file_key, text)

           try:
               with engine.connect() as connection:
                   query = sqltext(f"SELECT COUNT(*) FROM tweets_metadata WHERE ID = {row['ID']}")
                   result = connection.execute(query)
                   count = result.fetchone()[0]

                   if count == 0:  # Only insert if not already in DB
                       pd.DataFrame([metadata]).to_sql(
                           'tweets_metadata', engine, index=False, if_exists='append'
                       )
                       print(f"Inserted tweet {row['ID']} into RDS")
                   else:
                       print(f"Tweet {row['ID']} already exists in RDS")
           except SQLAlchemyError as e:
               print(f"Error inserting into RDS: {e}")

           # Mark as Processed
           processed_ids.add(row['ID'])

       # Wait before checking for new tweets
       time.sleep(interval)

# Call the Function
if __name__ == "__main__":
   process_tweets_to_s3_and_rds('/home/ubuntu/tweets.csv')
