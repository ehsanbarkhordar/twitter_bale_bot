import twitter

from main_config import Config

api = twitter.Api(consumer_key=Config.API_key,
                  consumer_secret=Config.API_secret_key,
                  access_token_key='1110445913791713280-2UYoQtPqZ5FhBX4fQfGHclShDtm64W',
                  access_token_secret='M9g1nOtTyqLQ5qA72AFwwjsv6tqHfyoHTJM2ujaw5PjNj',
                  tweet_mode='extended')
statuses = api.GetHomeTimeline(exclude_replies=True)
print(statuses)
