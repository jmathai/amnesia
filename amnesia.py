#!/usr/bin/env python
import csv
import sys
import time
from datetime import datetime, timedelta


from configs import twitter as twitter_config
from tweepy import API, Cursor, OAuthHandler
from tweepy.error import TweepError


# By default, actually delete tweet/likes.
# Set this to True to just print what will be deleted.
dry_run = twitter_config.get('dry_run', False)


if __name__ == "__main__":
    """
    Set up Twitter authentication
    """
    auth = OAuthHandler(twitter_config['consumer_key'],
                        twitter_config['consumer_secret'])
    auth.set_access_token(twitter_config['access_token'],
                          twitter_config['access_token_secret'])

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
    with open('tweets.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        # skip initial row
        line = 0
        for row in reader:
            if line == 0:
                pass
            else:
                status_id = row[0]
                status_created_at = datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S +0000")
                status_text = row[5]
                if status_created_at < delete_before:
                    try:
                        if not dry_run:
                            api.destroy_status(status_id)
                        print("Deleted {}".format(status_id))
                        print(status_text.encode('utf-8'))
                    except TweepError as err:
                        print("Could not delete {}".format(status_id))
            line += 1

    """
    Loop over your favorites.
    Compare the favorite's date with the threshold.
    If the favorite is older than the threshold we delete it.
    """
    # https://dev.twitter.com/rest/public/rate-limiting
    FIFTEEN_MINUTES = 15*60
    RATE_LIMIT = 180
    counter, elapsed_time, previous_time = 0, 0, 0

    for status in Cursor(api.favorites).items():
        if status.created_at < delete_before:
            try:
                if not dry_run:
                    api.destroy_favorite(status.id)
                print("Un-favorited {}".format(status.id))
                print(status.text.encode('utf-8'))
            except TweepError as err:
                print("Could not un-favorite {}".format(status.id))
            finally:
                # Sleep for a bit if we exceed the rate limit.
                current_time = time.time()
                previous_time = previous_time or current_time
                elapsed_time = current_time-previous_time
                previous_time = current_time
                counter += 1
                if elapsed_time < FIFTEEN_MINUTES and counter > RATE_LIMIT:
                    time.sleep(FIFTEEN_MINUTES-elapsed_time)
                    counter, elapsed_time, previous_time = 0, 0, 0


