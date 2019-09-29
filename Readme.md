# Amnesia for Twitter

This is a simple script that will automatically delete all of your tweets and
likes that are older than a specified number of days.
If you use Twitter for conversation and not posterity then you'll like Amnesia.

If you want a copy of your tweets for your own personal records, make sure you
[download your Twitter archive](https://help.twitter.com/en/managing-your-account/how-to-download-your-twitter-archive)
_before_ running Amnesia.

Remember: Amnesia cannot delete offline copies (e.g., screenshots, or web
crawling) of your tweets and likes.
Good luck.

## Requirements

You'll need the following.

  - Python 2.7 (3 probably works, too)
  - A Twitter App ([create one for free](https://apps.twitter.com/app/new))
  - OAuth tokens (get these after creating your app)

## Setting Amnesia Up

### Download Code and Dependencies

```
git clone https://github.com/jmathai/amnesia.git
cd amnesia
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### Configure Amnesia

You'll need to copy the `configs-sample.json` to `configs.json` and update the
oauth values.

```
cp configs-sample.json configs.json
```

The `delete_after_days` value specifies that you want to delete all tweets
older than that many days.

## Using Amnesia

### Running Amnesia

Unzip your Twitter archive, and copy `tweet.js` and `like.js` to this folder.

*By default, Amnesia will delete tweets/likes.* You may run it like so in a shell:

```bash
source venv/bin/activate
time amnesia.py &>> amnesia.log
```

And `tail -f amnesia.log` in another shell to monitor its progress.

### Cleaning up

If you like, you may
[revoke access](https://support.twitter.com/articles/76052)
to your Twitter account _after_ using Amnesia.

### Automating Amnesia

You may want to periodically run amnesia so that it keeps your tweets pruned.
I use my [crontab](https://en.wikipedia.org/wiki/Cron).
On Linux or OS X you can edit your crontab by typing `crontab -e` in a
terminal.

