import os

try:
    from local_config import LocalConfig

    bot_token = LocalConfig.bot_token
    consumer_key = LocalConfig.consumer_key
    consumer_secret = LocalConfig.consumer_secret
except ImportError:
    bot_toke = ""
    consumer_key = ""
    consumer_secret = ""


class BotConfig:
    rows_per_query = int(os.environ.get('ROWS_PER_QUERY', 50))
    max_retries = int(os.environ.get('MAX_RETRIES', 3))
    check_interval = float(os.environ.get('CHECK_INTERVAL', 0.5))
    time_sleep = float(os.environ.get('TIME_SLEEP', 0.5))
    max_perform_check_failure = int(os.environ.get('MAX_PERFORM_CHECK_FAILURE', 50))
    max_total_send_failure = int(os.environ.get('MAX_TOTAL_SEND_FAILURE', 10))
    active_next_limit = int(os.environ.get('ACTIVE_NEXT_LIMIT', 40))
    send_delay = float(os.environ.get('SEND_DELAY', 0.5))
    bot_token = os.environ.get('TOKEN', bot_token)
    bot_user_id = os.environ.get('USER_ID', "41")
    tweet_link = os.environ.get('TWITTER_STATUS_LINK', 'https://twitter.com/{screen_name}/status/{ID}')
    consumer_key = os.environ.get('CONSUMER_KEY', consumer_key)
    consumer_secret = os.environ.get('CONSUMER_SECRET', consumer_secret)
    tweet_count = int(os.environ.get('TWEET_COUNT', 3))


class DatabaseConfig:
    db_string_main = 'postgresql://{}:{}@{}:{}/{}'
    db_string = db_string_main.format(os.environ.get('POSTGRES_USER', "postgres"),
                                      os.environ.get('POSTGRES_PASSWORD', "123"),
                                      os.environ.get('POSTGRES_HOST', "localhost"),
                                      os.environ.get('POSTGRES_PORT', "5432"),
                                      os.environ.get('POSTGRES_DB', "twitter_bot"))
