def parse_timeline_messages(timeline):
    statuses = []

    for item in timeline:
        mined = {
            'tweet_id': item.id,
            'name': item.user.name,
            'screen_name': item.user.screen_name,
            'retweet_count': item.retweet_count,
            'text': item.full_text,
            'created_at': item.created_at,
            'favourite_count': item.favorite_count,
            'hashtags': item.entities['hashtags'],
            'status_count': item.user.statuses_count,
            'location': item.place,
            'source_device': item.source
        }
        try:
            mined['retweet_text'] = item.retweeted_status.full_text
        except:
            mined['retweet_text'] = 'None'
        try:
            mined['quote_text'] = item.quoted_status.full_text
            mined['quote_screen_name'] = item.quoted_status.user.screen_name
        except:
            mined['quote_text'] = 'None'
            mined['quote_screen_name'] = 'None'
        statuses.append(mined)
    return statuses
