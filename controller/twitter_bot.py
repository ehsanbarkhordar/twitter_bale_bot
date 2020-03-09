#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tweepy
from telegram import (ReplyKeyboardMarkup, Bot, Update)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
from telegram.ext import *
from constant.message import ReadyText, ButtonText
from db.models.user import User
from main_config import Config, logger
from twitter.twitter_api import auth

ACTION, REGISTER, TEXT, LOCATION, VERIFY_NUMBER = range(5)

back_keyboard = [[ButtonText.back]]
main_keyboard = [[ButtonText.send_tweet, ButtonText.get_home_time_line, ButtonText.search]]


def check_user_is_register():
    pass


def start(bot, update: Update, user_data):
    bale_id = str(update.effective_user.id)
    user = User.get_user_by_user_id(bale_id)
    if user:
        reply_keyboard = [[ButtonText.send_tweet, ButtonText.get_home_time_line, ButtonText.search]]
        update.message.reply_text(ReadyText.start_conversation.format(user.screen_name),
                                  reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard))
        user_data['user'] = user
        return ACTION
    else:
        reply_keyboard = [[ButtonText.register]]
        update.message.reply_text(ReadyText.need_registration,
                                  reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard))
        logger.info("need_registration")
        return REGISTER


def get_verify_url(bot, update):
    verify_link = auth.get_authorization_url()
    update.message.reply_text(ReadyText.send_verify_number.format(verify_link))
    return VERIFY_NUMBER


def register(bot, update: Update):
    user = update.effective_user
    message = update.effective_message
    try:
        auth.get_access_token(message.text)  # Replace XXXXXXX with verification code from URL
    except tweepy.TweepError:
        print('Verification Error')
    access_token = auth.access_token
    access_token_secret = auth.access_token_secret
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    try:
        twitter_user = api.me()
    except tweepy.TweepError:
        return REGISTER
    new_user = User(user.id, user.username, twitter_user.id, twitter_user.screen_name, access_token,
                    access_token_secret)
    User.add_new_user(new_user)
    update.message.reply_text(ReadyText.success_insert_user, reply_markup=ReplyKeyboardMarkup(keyboard=main_keyboard))
    return ACTION


def get_tweet_msg(bot, update, user_data):
    logger.info("in gender")
    # user = update.message.from_user
    # logger.info("Gender of %s: %s", user.first_name, update.message.text)

    update.message.reply_text(ReadyText.send_text_twitter, reply_markup=ReplyKeyboardMarkup(keyboard=back_keyboard))
    return TEXT


def send_tweet(bot, update, user_data):
    logger.info("in gender")
    # user = update.message.from_user
    # logger.info("Gender of %s: %s", user.first_name, update.message.text)
    user = user_data['user']
    auth.set_access_token(user.access_token, user.access_token_secret)
    api = tweepy.API(auth)
    api.update_status('Test Tweet')
    update.message.reply_text(ReadyText.success_tweet, reply_markup=ReplyKeyboardMarkup(keyboard=back_keyboard))
    return ConversationHandler.END


def get_time_line(bot, update):
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    logger.info(photo_file)
    photo_file.download('user_photo.jpg')
    logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
    update.message.reply_text('Gorgeous! Now, send me your location please, '
                              'or send /skip if you don\'t want to.')
    return LOCATION


def search(bot, update, user_data):
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text('I bet you look great! Now, send me your location please, '
                              'or send /skip.')

    return LOCATION


def location(bot, update):
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    update.message.reply_text('Maybe I can visit you sometime! '
                              'At last, tell me something about yourself.')

    return VERIFY_NUMBER


def skip_location(bot, update):
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    update.message.reply_text('You seem a bit paranoid! '
                              'At last, tell me something about yourself.')

    return VERIFY_NUMBER


def bio(bot, update):
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Thank you! I hope we can talk again some day.')

    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.')

    return ConversationHandler.END


def error(bot, update):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, update.message)


def main():
    # Create the Updater and pass it your bot's token.
    bot = Bot(token=Config.bot_token,
              base_url=Config.base_url,
              base_file_url=Config.base_file_url)
    updater = Updater(bot=bot)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    back_regex = RegexHandler(pattern='^' + ButtonText.back + '$', callback=start)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start, pass_user_data=True),
                      MessageHandler(Filters.all, callback=start)],

        states={
            ACTION: [
                back_regex,
                RegexHandler(pattern='^' + ButtonText.send_tweet + '$', callback=get_tweet_msg, pass_user_data=True),
                RegexHandler(pattern='^' + ButtonText.get_home_time_line + '$', callback=get_tweet_msg,
                             pass_user_data=True),
                RegexHandler(pattern='^' + ButtonText.search + '$', callback=search, pass_user_data=True)],
            REGISTER: [back_regex,
                       RegexHandler(pattern='^' + ButtonText.register + '$', callback=get_verify_url)],
            VERIFY_NUMBER: [back_regex,
                            MessageHandler(Filters.text, register)],
            TEXT: [back_regex,
                   MessageHandler(Filters.text, send_tweet)],

            LOCATION: [back_regex,
                       MessageHandler(Filters.location, location),
                       CommandHandler('skip', skip_location)],
            #
            # VERIFY_NUMBER: [back_regex,
            #                 MessageHandler(Filters.text, bio)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # dp.add_handler(RegexHandler(pattern='^' + ButtonText.send_tweet + '$', callback=get_tweet_msg))
    # dp.add_handler(RegexHandler(pattern='^' + ButtonText.get_home_time_line + '$', callback=get_tweet_msg))
    # dp.add_handler(RegexHandler(pattern='^' + ButtonText.search + '$', callback=search))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling(poll_interval=2)
    # you can replace above line with commented below lines to use webhook instead of polling
    # updater.bot.set_webhook(url="{}{}".format(os.getenv('WEB_HOOK_DOMAIN', "https://testwebhook.bale.ai"),
    #                                           os.getenv('WEB_HOOK_PATH', "/get-upd")))
    # updater.start_webhook(listen=os.getenv('WEB_HOOK_IP', ""), port=int(os.getenv('WEB_HOOK_PORT', "")),
    #                       url_path=os.getenv('WEB_HOOK_PATH', ""))

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
