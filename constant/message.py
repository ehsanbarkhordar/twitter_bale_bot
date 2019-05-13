class ReadyText:
    start_conversation = "{} سلام.\n" \
                         "به بازو *توییتر همراه* خوش آمدید. لطفا یکی از گزینه های زیر را انتخاب کنید."
    you_should_register_first = "سلام!\n" \
                                "به بازو *توییتر همراه* خوش آمدید.\n" \
                                "برای استفاده از امکانات این بازو شما نیاز به ثبت نام دارید."

    send_verify_number = "لطفا وارد لینک زیر شوید و عدد دریافتی را برای من بفرستید.\n" \
                         "{}"
    send_text_twitter = "لطفا متن توییت خود را ارسال کنید.\n" \
                        "*توجه:* ممکن است ارسال توییت کمی زمان‌بر باشد. از شکیبایی شما متشکریم"
    send_search_text = "لطفا متن مورد نظر برای جست و جو را وارد نمایید."
    success_tweet = "توییت شما با موفقیت ارسال گردید."
    fail_tweet = "متاسفانه! ارسال توییت موفق نبود."
    error = "*متاسفانه، خطایی رخ داده است. *\n" \
            " لطفا دوباره سعی کنید."
    information = "بازویی برای استفاده آسان از توییتر در پیام رسان بله"
    send_name = "لطفا نام خود را ارسال کنید."
    send_phone_number = "لطفا تلفن همراه خود را ارسال کنید."
    success_insert_user = "نام شما با موفقیت در بازو ثبت شد."
    failure_insert_user = "متاسفانه نام شما با موفقیت در بازو ثبت نشد.\nلطفا دوباره سعی کنید."
    need_registration = "برای استفاده از امکانات این بازو شما نیاز به *ثبت نام* دارید.\n" \
                        "لطفا، برای ثبت اکانت توییتر خود روی دکمه زیر کلیک کنید."
    status_text = "{full_text}\n" \
                  "[لینک توییت]" \
                  "({tweet_link})\n" \
                  "*لایک* : {favorite_count} -- *ریتویت* : {re_tweet_count}" \
                  "\n{created_at}"
    register_before = "شما قبلا ثبت نام کرده اید."
    anonymous = "کاربر ناشناس"
    no_search_result = "هیچ توییتی پیدا نشد!"


class ButtonText:
    cancel = "لغو"
    keep_on = "تایید و ادامه"
    edit = "اصلاح میکنم"
    start = "ادامه"
    info = "راهنما"
    back = "بازگشت به منو اصلی"
    send_tweet = "ارسال تويیت"
    get_home_time_line = "خواندن تایم لاین"
    register = "ثبت نام"
    search = "جستجو توییت"
    show_more = "موارد بیشتر"


class LogMessage:
    success_send_message = "success send message"
    failure_send_message = "failure send message"
    max_fail_retried = "max fails retried"
    upload_failure = "upload was failed"
    upload_success = "upload was successful"
    info = "info showed"


class RegexPattern:
    score_regex = '(^[0-9]+)$|(^[۰-۹]+)$'
