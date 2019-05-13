from balebot.filters import TemplateResponseFilter, TextFilter, DefaultFilter
from balebot.handlers import MessageHandler, CommandHandler
from balebot.models.messages import TemplateMessageButton, TextMessage, TemplateMessage
from balebot.updater import Updater

from constant.tweet_message import get_status_message
from main_config import BotConfig
from constant.message import ButtonText, LogMessage
from db.models.user import *
import asyncio

from twitter.twitter_api import get_verify_link, send_tweet_api, final_verify, search_api, home_time_line

updater = Updater(token=BotConfig.bot_token, loop=asyncio.get_event_loop())
dispatcher = updater.dispatcher

logger = Logger.logger


# =================================== Call Backs =======================================================

def success_send_message(response, user_data):
    kwargs = user_data['kwargs']
    update = kwargs["update"]
    user_peer = update.get_effective_user()
    logger.info(LogMessage.success_send_message, extra={"user_id": user_peer.peer_id, "tag": "info"})


def failure_send_message(response, user_data):
    kwargs = user_data['kwargs']
    bot = kwargs["bot"]
    message = kwargs["message"]
    update = kwargs["update"]
    try_times = int(kwargs["try_times"])
    if try_times < BotConfig.max_total_send_failure:
        try_times += 1
        user_peer = update.get_effective_user()
        logger.error(LogMessage.failure_send_message, extra={"user_id": user_peer.peer_id, "tag": "error"})
        kwargs = {"message": message, "update": update, "bot": bot, "try_times": try_times}
        bot.respond(update=update, message=message, success_callback=success_send_message,
                    failure_callback=failure_send_message, kwargs=kwargs)
    else:
        logger.error(LogMessage.max_fail_retried, extra={"tag": "error"})


def success_send_message_and_start_again(response, user_data):
    kwargs = user_data['kwargs']
    update = kwargs["update"]
    bot = kwargs["bot"]
    user_peer = update.get_effective_user()
    logger.info(LogMessage.success_send_message, extra={"user_id": user_peer.peer_id, "tag": "info"})
    start_conversation(bot, update)


main_menu = [TemplateMessageButton(text=ButtonText.send_tweet, value=ButtonText.send_tweet, action=0),
             TemplateMessageButton(text=ButtonText.get_home_time_line, value=ButtonText.get_home_time_line, action=0),
             TemplateMessageButton(text=ButtonText.search, value=ButtonText.search, action=0),
             TemplateMessageButton(text=ButtonText.info, value=ButtonText.info, action=0)]

register = [TemplateMessageButton(text=ButtonText.register, value=ButtonText.register, action=0)]


# =================================== Main Bot =======================================================

def get_registered_user(bot, update):
    user_peer = update.get_effective_user()
    user = User.get_user_by_peer_id(user_peer.peer_id)
    if user:
        return user
    else:
        general_message = TextMessage(ReadyText.need_registration)
        btn_list = [TemplateMessageButton(text=ButtonText.register)]
        template_message = TemplateMessage(general_message=general_message, btn_list=btn_list)
        kwargs = {"message": template_message, "update": update, "bot": bot, "try_times": 1}
        bot.send_message(template_message, user_peer, success_callback=success_send_message,
                         failure_callback=failure_send_message, kwargs=kwargs)
        dispatcher.finish_conversation(update)
        return False


@dispatcher.message_handler(filters=[DefaultFilter()])
def start_conversation(bot, update):
    user_peer = update.get_effective_user()
    user = User.get_user_by_peer_id(user_peer.peer_id)
    if user and isinstance(user, User):
        general_message = TextMessage(ReadyText.start_conversation.format(user.screen_name))
        template_message = TemplateMessage(general_message=general_message, btn_list=main_menu)
    else:
        general_message = TextMessage(ReadyText.you_should_register_first)
        template_message = TemplateMessage(general_message=general_message, btn_list=register)
    kwargs = {"message": template_message, "update": update, "bot": bot, "try_times": 1}
    bot.send_message(template_message, user_peer, success_callback=success_send_message,
                     failure_callback=failure_send_message, kwargs=kwargs)
    dispatcher.finish_conversation(update)


@dispatcher.message_handler(TemplateResponseFilter(keywords=[ButtonText.register]))
def registration(bot, update):
    dispatcher.clear_conversation_data(update)
    user_peer = update.get_effective_user()
    auth = get_verify_link()
    dispatcher.set_conversation_data(update, "auth", auth)
    verify_link = auth['auth_url']
    text_message = TextMessage(ReadyText.send_verify_number.format(verify_link))
    kwargs = {"message": text_message, "update": update, "bot": bot, "try_times": 1}
    bot.send_message(text_message, user_peer, success_callback=success_send_message,
                     failure_callback=failure_send_message, kwargs=kwargs)
    dispatcher.register_conversation_next_step_handler(
        update, common_handlers + [MessageHandler(TextFilter(), verify),
                                   MessageHandler(DefaultFilter(), start_conversation)])


def verify(bot, update):
    user_peer = update.get_effective_user()
    auth = dispatcher.get_conversation_data(update, "auth")
    oauth_verifier = update.get_effective_message().text
    final_dict = final_verify(oauth_verifier=oauth_verifier, auth=auth)
    new_user = User(peer_id=int(user_peer.peer_id), access_hash=user_peer.access_hash,
                    twitter_user_id=final_dict.get('user_id'),
                    screen_name=final_dict.get('screen_name'), oauth_token=final_dict.get('oauth_token'),
                    oauth_token_secret=final_dict.get('oauth_token_secret'))
    result = User.add_new_user(new_user)
    if result and result == ReadyText.register_before:
        general_message = TextMessage(ReadyText.register_before)
    elif result:
        general_message = TextMessage(ReadyText.success_insert_user)
    else:
        general_message = TextMessage(ReadyText.failure_insert_user)
    message = TemplateMessage(general_message=general_message, btn_list=main_menu)
    kwargs = {"message": message, "update": update, "bot": bot, "try_times": 1}
    bot.send_message(message, user_peer, success_callback=success_send_message,
                     failure_callback=failure_send_message, kwargs=kwargs)
    dispatcher.finish_conversation(update)


@dispatcher.message_handler(TemplateResponseFilter(keywords=[ButtonText.send_tweet]))
def get_tweet_text(bot, update):
    user_peer = update.get_effective_user()
    user = get_registered_user(bot, update)
    if user:
        dispatcher.set_conversation_data(update, "user", user)
        general_message = TextMessage(ReadyText.send_text_twitter)
        btn_list = [TemplateMessageButton(text=ButtonText.cancel, value=ButtonText.cancel, action=0)]
        template_message = TemplateMessage(general_message=general_message, btn_list=btn_list)
        kwargs = {"message": template_message, "update": update, "bot": bot, "try_times": 1}
        bot.send_message(template_message, user_peer, success_callback=success_send_message,
                         failure_callback=failure_send_message, kwargs=kwargs)
        dispatcher.register_conversation_next_step_handler(
            update, common_handlers + [MessageHandler(TextFilter(), send_tweet),
                                       MessageHandler(DefaultFilter(), start_conversation)])


def send_tweet(bot, update):
    user_peer = update.get_effective_user()
    tweet_text = update.get_effective_message().text
    user = dispatcher.get_conversation_data(update, "user")
    if send_tweet_api(user=user, tweet_text=tweet_text):
        general_message = TextMessage(ReadyText.success_tweet)
    else:
        general_message = TextMessage(ReadyText.fail_tweet)
    btn_list = [TemplateMessageButton(text=ButtonText.back, value=ButtonText.back, action=0)]
    template_message = TemplateMessage(general_message=general_message, btn_list=btn_list)
    kwargs = {"message": template_message, "update": update, "bot": bot, "try_times": 1}
    bot.send_message(template_message, user_peer, success_callback=success_send_message,
                     failure_callback=failure_send_message, kwargs=kwargs)
    dispatcher.finish_conversation(update)


def send_status_message(id_index, loop, statuses, bot, update):
    user_peer = update.get_effective_user()
    if id_index == len(statuses) - 1:
        btn_list = [TemplateMessageButton(text=ButtonText.show_more, value=ButtonText.show_more, action=0),
                    TemplateMessageButton(text=ButtonText.back, value=ButtonText.back, action=0)]
        status = statuses[id_index]
        status_text = get_status_message(status)
        message = TextMessage(status_text)
        template_message = TemplateMessage(general_message=message, btn_list=btn_list)
        kwargs = {"message": template_message, "update": update, "bot": bot, "try_times": 1}
        bot.send_message(template_message, user_peer, success_callback=success_send_message,
                         failure_callback=failure_send_message, kwargs=kwargs)
        return 0
    status = statuses[id_index]
    status_text = get_status_message(status)
    message = TextMessage(status_text)
    kwargs = {"message": message, "update": update, "bot": bot, "try_times": 1}
    bot.send_message(message, user_peer, success_callback=success_send_message,
                     failure_callback=failure_send_message, kwargs=kwargs)
    id_index += 1
    loop.call_later(BotConfig.send_delay, send_status_message, id_index, loop, statuses, bot, update)


@dispatcher.message_handler(TemplateResponseFilter(keywords=[ButtonText.get_home_time_line, ButtonText.show_more]))
def get_home_time_line(bot, update):
    user = get_registered_user(bot, update)
    if user:
        time_line = home_time_line(user=user)
        loop = asyncio.get_event_loop()
        loop.call_soon(send_status_message, 0, loop, time_line, bot, update)
        dispatcher.finish_conversation(update)


@dispatcher.message_handler(TemplateResponseFilter(keywords=[ButtonText.search]))
def get_search_text(bot, update):
    user_peer = update.get_effective_user()
    user = get_registered_user(bot, update)
    if user:
        dispatcher.set_conversation_data(update, "user", user)
        text_message = TextMessage(ReadyText.send_search_text)
        kwargs = {"message": text_message, "update": update, "bot": bot, "try_times": 1}
        bot.send_message(text_message, user_peer, success_callback=success_send_message,
                         failure_callback=failure_send_message, kwargs=kwargs)
        dispatcher.register_conversation_next_step_handler(
            update, common_handlers + [MessageHandler(TextFilter(), search_tweets),
                                       MessageHandler(DefaultFilter(), start_conversation)])


def search_tweets(bot, update):
    query = update.get_effective_message().text
    user = dispatcher.get_conversation_data(update, "user")
    statuses = search_api(user=user, query=query)

    statuses = statuses.get("statuses")
    if statuses:
        loop = asyncio.get_event_loop()
        loop.call_soon(send_status_message, 0, loop, statuses, bot, update)
        dispatcher.finish_conversation(update)
    else:
        btn_list = [TemplateMessageButton(text=ButtonText.back, value=ButtonText.back, action=0)]
        general_message = TextMessage(ReadyText.no_search_result)
        template_message = TemplateMessage(general_message=general_message, btn_list=btn_list)
        kwargs = {"message": template_message, "update": update, "bot": bot, "try_times": 1}
        bot.respond(update, template_message, success_callback=success_send_message,
                    failure_callback=failure_send_message, kwargs=kwargs)
        dispatcher.finish_conversation(update)


@dispatcher.message_handler(TemplateResponseFilter(keywords=[ButtonText.info]))
def info(bot, update):
    btn_list = [TemplateMessageButton(text=ButtonText.back, value=ButtonText.back, action=0)]
    general_message = TextMessage(ReadyText.information)
    template_message = TemplateMessage(general_message=general_message, btn_list=btn_list)
    kwargs = {"message": template_message, "update": update, "bot": bot, "try_times": 1}
    bot.respond(update, template_message, success_callback=success_send_message,
                failure_callback=failure_send_message, kwargs=kwargs)
    dispatcher.finish_conversation(update)


# =================================== Handlers =========================================
common_handlers = [
    MessageHandler(filters=TemplateResponseFilter(keywords=[ButtonText.back]), callback=start_conversation),
    CommandHandler(commands="start", callback=start_conversation, include_template_response=True)]
