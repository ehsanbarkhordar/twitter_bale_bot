from balebot.utils.logger import Logger
from twython import Twython, TwythonError
from main_config import BotConfig

logger = Logger.get_logger()
consumer_key = BotConfig.consumer_key
consumer_secret = BotConfig.consumer_secret


def twitter_persist(func):
    def persist(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            logger.info("twitter api: " + func.__name__)
            return res
        except TwythonError as e:
            logger.error(e.args)
            return False

    return persist


@twitter_persist
def get_verify_link():
    twitter = Twython(consumer_key, consumer_secret)
    auth = twitter.get_authentication_tokens()
    return auth


@twitter_persist
def final_verify(oauth_verifier, auth):
    twitter = Twython(consumer_key, consumer_secret, auth['oauth_token'], auth['oauth_token_secret'])
    final_step = twitter.get_authorized_tokens(oauth_verifier)
    return final_step


@twitter_persist
def send_tweet_api(user, tweet_text):
    twitter = Twython(consumer_key, consumer_secret, user.oauth_token, user.oauth_token_secret)
    result = twitter.update_status(status=tweet_text)
    return result


@twitter_persist
def home_time_line(user):
    twitter = Twython(consumer_key, consumer_secret, user.oauth_token, user.oauth_token_secret)
    result = twitter.get_home_timeline(count=BotConfig.tweet_count, tweet_mode='extended')
    return result


@twitter_persist
def search_api(user, query):
    twitter = Twython(consumer_key, consumer_secret, user.oauth_token, user.oauth_token_secret)
    result = twitter.search(q=query, count=BotConfig.tweet_count, tweet_mode='extended')
    return result
