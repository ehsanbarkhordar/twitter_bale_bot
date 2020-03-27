import tweepy

from main_config import Config

auth = tweepy.OAuthHandler(Config.API_key, Config.API_secret_key)


def get_verify_link():

    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        raise tweepy.TweepError
    return redirect_url



#
# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet.text)

