#!/usr/bin/env python
import configparser
import os

config = configparser.ConfigParser()
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, './config.ini')
config.read(filename)


class Config:
    # bot
    rows_per_query = int(os.environ.get('ROWS_PER_QUERY', 50))
    max_retries = int(os.environ.get('MAX_RETRIES', 3))
    check_interval = float(os.environ.get('CHECK_INTERVAL', 0.5))
    time_sleep = float(os.environ.get('TIME_SLEEP', 0.5))
    max_perform_check_failure = int(os.environ.get('MAX_PERFORM_CHECK_FAILURE', 50))
    max_total_send_failure = int(os.environ.get('MAX_TOTAL_SEND_FAILURE', 10))
    active_next_limit = int(os.environ.get('ACTIVE_NEXT_LIMIT', 40))
    send_delay = float(os.environ.get('SEND_DELAY', 0.5))
    bot_token = os.environ.get('TOKEN', config['bot']['token'])
    bot_user_id = os.environ.get('USER_ID', "41")
    # twitter
    tweet_link = os.environ.get('TWITTER_STATUS_LINK', 'https://twitter.com/{screen_name}/status/{ID}')
    tweet_count = int(os.environ.get('TWEET_COUNT', 3))
    API_key = os.environ.get('API_KEY', config['twitter']['API_key'])
    API_secret_key = os.environ.get('API_SECRET_KEY', config['twitter']['API_secret_key'])
    my_access_token = os.environ.get('MY_ACCESS_TOKEN', config['my-tokens']['access_token'])
    my_access_token_secret = os.environ.get('MY_ACCESS_TOKEN_SECRET', config['my-tokens']['access_token_secret'])

    # database
    db_string_main = 'postgresql://{}:{}@{}:{}/{}'
    db_string = db_string_main.format(os.environ.get('POSTGRES_USER', config['postgres']['user']),
                                      os.environ.get('POSTGRES_PASSWORD', config['postgres']['password']),
                                      os.environ.get('POSTGRES_HOST', config['postgres']['host']),
                                      os.environ.get('POSTGRES_PORT', config['postgres']['port']),
                                      os.environ.get('POSTGRES_DB', config['postgres']['db']))
