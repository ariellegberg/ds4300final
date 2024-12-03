import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def get_sentiment_label(text, analyzer):
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']
    if compound >= 0.05:
        return 'Positive'
    elif compound <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'


def vader_manual_labeling(input_csv='/Users/arielle/ds4300final/tweets.csv', output_csv='sentiment_tweets.csv',
                          text_column='Text', required_columns=None, limit=None):
    if required_columns is None:
        required_columns = ['ID', 'User', 'Text', 'Sentiment']

    analyzer = SentimentIntensityAnalyzer()
    df = pd.read_csv(input_csv, encoding='latin1')

    # Validate the required columns
    missing_columns = [col for col in required_columns if col != 'Sentiment' and col not in df.columns]
    if missing_columns:
        raise ValueError(f"The following required columns are missing in the input CSV: {missing_columns}")

    # Apply sentiment analysis to the specified number of rows
    if limit:
        df = df.head(limit)

    df['Sentiment'] = df[text_column].apply(lambda text: get_sentiment_label(text, analyzer))

    # Filter only the required columns
    output_df = df[required_columns]

    output_df.to_csv(output_csv, index=False)
    print(f"Sentiment analysis complete. Saved to {output_csv}.")


vader_manual_labeling()
