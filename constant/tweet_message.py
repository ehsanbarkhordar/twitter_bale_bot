import datetime

import persian as persian
from constant.message import ReadyText
from main_config import BotConfig
from khayyam3 import *


# def make_tweet_message(user_name, text, profile_image_url, favorite_count, retweet_count):
#     message = TextMessage(
#         ReadyText.tweet_message.format(text, user_name, favorite_count, retweet_count,
#                                        profile_image_url))
#     return message

#
# def extend_tweets(tweets):
#     tweets_list = []
#     for tweet in tweets:
#         user = tweet.get("user")
#         print(tweet)
#         retweeted_status = tweet.get("retweeted_status")
#         if retweeted_status:
#             favorite_count = retweeted_status.get("favorite_count")
#         else:
#             favorite_count = tweet.get("favorite_count")
#         entities = tweet.get("entities")
#         media = entities.get("media")
#         if media:
#             media = media[0]
#             media_url = media.get("media_url")
#             sizes = media.get("sizes")
#             medium = sizes.get("medium")
#             height = medium.get("h")
#             width = medium.get("w")
#             media_dict = {"media_url": media.get("media_url"), "height": height, "width": width}
#         else:
#             media_dict = {}
#         dict = {"name": user.get("name"), "text": tweet.get("text"),
#                 "screen_name": "https://twitter.com/" + user.get("screen_name"),
#                 "tweet_link": "https://twitter.com/statuses/" + tweet.get("id_str"),
#                 "profile_image_url": user.get("profile_image_url"),
#                 "favorite_count": favorite_count,
#                 "retweet_count": tweet.get("retweet_count"),
#                 "datetime": datetime_converter(tweet.get("created_at", None)),
#                 "media_dict": media_dict
#                 }
#
#         tweets_list.append(dict)
#     return tweets_list


def get_status_message(status):
    user = status['user']
    screen_name = user['screen_name']
    name = user['name']
    tweet_link = BotConfig.tweet_link.format(screen_name=screen_name, ID=status['id_str'])
    full_text = status['full_text']
    re_tweeted_status = status.get('retweeted_status')
    if re_tweeted_status:
        favorite_count = re_tweeted_status['favorite_count']
        re_tweet_user = re_tweeted_status['user']
        retweet_name = ReadyText.retweet_from.format(re_tweet_user['name'])
    else:
        favorite_count = status['favorite_count']
        retweet_name = ""
    favorite_count = persian.convert_en_numbers(favorite_count)
    re_tweet_count = status['retweet_count']
    re_tweet_count = persian.convert_en_numbers(re_tweet_count)
    created_at = status['created_at']
    datetime_utc = datetime.datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")
    created_at = JalaliDatetime().from_datetime(datetime_utc).strftime('%C')
    created_at = persian.convert_en_numbers(created_at)
    return ReadyText.status_text.format(name=name, retweet_name=retweet_name, full_text=full_text,
                                        tweet_link=tweet_link,
                                        favorite_count=favorite_count,
                                        re_tweet_count=re_tweet_count,
                                        created_at=created_at)


def get_status_media(status):
    media_dict = status.get("media_dict")
    if media_dict:
        media_url = media_dict.get("media_url")
        # print(media_url)
        # import ast
        # media_url = ast.literal_eval(media_url)
        # print(media_url)
        height = media_url.get("height")
        width = media_url.get("width")
        #
        # def file_upload_success(result, user_data):
        #     print("upload was successful : ", result)
        #     print(user_data)
        #     file_id = str(user_data.get("file_id", None))
        #     access_hash = str(user_data.get("user_id", None))
        #     file_size = str(user_data.get("file_size", None))
        #
        #     photo_message = PhotoMessage(file_id=file_id, access_hash=access_hash, name="Bale",
        #                                  file_size='11337',
        #                                  mime_type="image/jpeg", caption_text=TextMessage(text="Bale"),
        #                                  file_storage_version=1, thumb=None)
        #
        #     bot.send_message(photo_message, user_peer, success_callback=success_send_message,
        #                      failure_callback=failure_send_message)
        #
        # bot.upload_file(file="media_url", file_type="file", success_callback=file_upload_success,
        #                 failure_callback=failure_send_message)
