import tweepy

from main_config import Config

auth = tweepy.OAuthHandler(Config.API_key, Config.API_secret_key)
auth.set_access_token(Config.my_access_token, Config.my_access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)
