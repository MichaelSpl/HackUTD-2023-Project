import praw as prw
import matplotlib.pyplot as plt
import datetime as dt

# getting info for the Reddit API, mostly credentials
user_agent = "Scraper by /u/nex012"
reddit = prw.Reddit(client_id="ESu14gEWC8ehWsZP7B-Bsg",
                    client_secret="5oASuJGaj64RfkEkgAX6Waj8clmigg",
                    user_agent=user_agent)

# list of words to look for in the comment section of matching posts
sentiment_keywords = {
    "positive": ["upward", "trend", "buy", "profitable", "growth", "gains", "increase"],
    "neutral": ["wait", "hold", "steady", "straight", "sideways"],
    "negative": ["short", "loss", "down", "poor", "broke", "decrease"]
}

# list of the top 20 companies to search after in the subreddit
top10 = {
    "Amazon": ['AMZN'], "Apple": ['AAPL', 'Apple Inc.'],
    "Tesla": ['TSLA'], "Google": ['GOOGL', 'Alphabet Inc.'],
    "AMD": ['AMD', 'Advanced Micro Devices'],
    "AMC": ['AMC', 'AMC Entertainment']

}

current_time = dt.datetime.now()
comp_sentiments = {company: {sentiment: [] for sentiment in sentiment_keywords} for company in top10}
comment_count = 0
one_week_ago = current_time - dt.timedelta(7)
normalized_constant = 0.1
max_posts = 10
max_comments = 25
x_values = {company: [] for company in top10}
y_values = {company: [] for company in top10}


for company, mentions in top10.items():
    for mention in mentions:
        posts_count = 0;
        for submission in reddit.subreddit("StockMarket").search(mention, time_filter="week"):
            if dt.datetime.fromtimestamp(submission.created_utc) < one_week_ago:
                break
            submission.comments.replace_more(limit=None)
            comments_read = 0

            for comment in submission.comments.list():
                if comments_read >= max_comments:
                    break
                comment_body = comment.body.lower()
                sentiment_values = {sentiment: 0 for sentiment in sentiment_keywords}
                for sentiment, keywords in sentiment_keywords.items():
                    for keyword in keywords:
                        if keyword in comment_body:
                            sentiment_values[sentiment] = 1
                            break
                for sentiment, value in sentiment_values.items():
                    comp_sentiments[company][sentiment].append(value)

                comments_read += 1
            posts_count += 1

            if posts_count >= max_posts:
                break

def normalize_sentiment(value):
    return (value + 1) / 2

for company, sentiments in comp_sentiments.items():
    for sentiment, values in sentiments.items():
        if values:
            # Normalize the sentiment values
            normalized_values = [normalize_sentiment(value) for value in values]

            plt.figure()
            plt.plot(normalized_values, label=f"{sentiment} Sentiment")
            plt.title(f"Sentiment Analysis for {company}")
            plt.xlabel("Comment count")
            plt.ylabel("Normalized Sentiment Value")
            plt.legend()

plt.show()
