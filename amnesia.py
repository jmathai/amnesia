#!/usr/bin/env python
import sys
from datetime import datetime, timedelta


from configs import twitter as twitter_config
from tweepy import API, Cursor, OAuthHandler
from tweepy.error import TweepError


if __name__ == "__main__":
    """
    Set up Twitter authentication
    """
    auth = OAuthHandler(twitter_config['consumer_key'], twitter_config['consumer_secret'])
    auth.set_access_token(twitter_config['access_token'], twitter_config['access_token_secret'])

    """
    Create api module using authentication.
    """
    api = API(auth)
    try:
        verify = api.verify_credentials()
        user_id = verify.id
    except TweepError as err:
        print(err)
        print('Authentication Error')
        sys.exit(0)

    """
    Tweets before this date will be deleted.
    It's today minus `twitter_config['delete_after_days']` days
    """
    days = timedelta(days=twitter_config['delete_after_days'])
    delete_before = datetime.now() - days

    """
    Loop over your timeline.
    Compare the tweet's date with the threshold.
    If the tweet is older than the threshold we delete it.
    """
    for status in Cursor(api.user_timeline).items():
        if status.created_at < delete_before:
            try:
                api.destroy_status(status.id)
                print("Deleted {}".format(status.id))
                print(status.text.encode('utf-8'))
            except TweepError as err:
                print("Could not delete {}".format(status.id))

    """
    Loop over your favorites.
    Compare the favorite's date with the threshold.
    If the favorite is older than the threshold we delete it.
    """
    for status in Cursor(api.favorites).items():
        if status.created_at < delete_before:
            try:
                api.destroy_favorite(status.id)
                print("Un-favorited {}".format(status.id))
                print(status.text.encode('utf-8'))
            except TweepError as err:
                print("Could not un-favorite {}".format(status.id))
