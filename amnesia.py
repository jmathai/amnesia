#!/usr/bin/env python3
import json
import sys
import time
from datetime import datetime, timedelta


from tweepy import API, OAuthHandler
from tweepy.error import TweepError


def init_api(consumer_key, consumer_secret, access_token, access_token_secret):
    # Set up Twitter authentication.
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Create API module using authentication.
    api = API(auth)
    try:
        verify = api.verify_credentials()
        user_id = verify.id
    except TweepError as err:
        print(err)
        print("Authentication Error")
        sys.exit(1)
    else:
        return api


def del_tweets(api, delete_after_days):
    # Tweets before this date will be deleted.
    # It"s today minus delete_after_days days.
    days = timedelta(days=delete_after_days)
    delete_before = datetime.now() - days

    # Loop over your timeline.
    # Compare the tweet"s date with the threshold.
    # If the tweet is older than the threshold we delete it.
    with open("tweet.js") as tweet_js:
        TWEET_PREFIX = "window.YTD.tweet.part0 = "
        tweet_js = tweet_js.read()
        assert tweet_js.startswith(TWEET_PREFIX)
        tweet_json = tweet_js[len(TWEET_PREFIX):]
        tweets = json.loads(tweet_json)

        for tweet in tweets:
            status_id = tweet["id"]
            status_created_at = datetime.strptime(tweet["created_at"], "%a %b %d %H:%M:%S +0000 %Y")
            status_text = tweet["full_text"]

            if status_created_at < delete_before:
                try:
                    api.destroy_status(status_id)
                    print("Deleted {}: {}".format(status_id, status_text.encode("unicode_escape")))
                except TweepError as err:
                    print("Could not delete {}".format(status_id))


def del_likes(api):
    # Loop over your favorites, and delete them.
    with open("like.js") as like_js:
        LIKE_PREFIX = "window.YTD.like.part0 = "
        like_js = like_js.read()
        assert like_js.startswith(LIKE_PREFIX)
        like_json = like_js[len(LIKE_PREFIX):]
        likes = json.loads(like_json)

        while len(likes):
            like = likes.pop()
            like = like["like"]
            status_id = like["tweetId"]
            status_text = like["fullText"]

            try:
                api.destroy_favorite(status_id)
                print("Unliked {}: {}".format(status_id, status_text.encode("unicode_escape")))
            except TweepError as err:
                errors = err.response.json()["errors"]
                print("Could not unlike {}: {}".format(status_id, errors))
                # https://dev.twitter.com/rest/public/rate-limiting
                if any(e["code"] == 88 for e in errors):
                    print("Sleeping for 15m...")
                    time.sleep(15*60)


if __name__ == "__main__":
    with open("configs.json") as configs_json:
        c = json.load(configs_json)
        api = init_api(c["consumer_key"], c["consumer_secret"], c["access_token"], c["access_token_secret"])
        #del_tweets(api, c["delete_after_days"])
        del_likes(api)

