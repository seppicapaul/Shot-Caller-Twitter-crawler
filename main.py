import time

import tweepy
import csv
import mysql.connector

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="deven",
    password="",
    port="3306",
    database="twitter_data",
    use_unicode=True,
    charset="utf8mb4"
)

mycursor = mydb.cursor()

auth = tweepy.OAuthHandler("T0jUhEpTK0BzFqbXqAHSMAQ3V", "KQb2Sqz7XhNXvzvkp41JUF29QoAgpUrbMJrh5YOJoPO2hjCpnx")
auth.set_access_token("1264291102347063297-kxNwByeBVXHFYe6QWaOR4aeJk49bAh",
                      "wM3DgJWpIoodGkClTMMQoTHPTTJFgxIp1ccIVg2q3exe0")

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# twitterHandles = []
# twitterHandles.append("elonmusk")

filename = open('/home/deven/shotcaller-twitter/influencers_of_crypto_youtube.csv')
file = csv.DictReader(filename)
twitterHandles = []

for col in file:
    if col['Twitter Handle'] != "":
        col['Twitter Handle'] = col['Twitter Handle'].strip('@')
        col['Twitter Handle'] = col['Twitter Handle'].strip('\n')
        twitterHandles.append(col['Twitter Handle'])

# for handle in twitterHandles:
#     print("Twitter handle: " + handle)

# for handle in twitterHandles:
#     user = api.get_user(handle)
#     print("User: " + user.name + ", Twitter handle: " + handle)

for handle in twitterHandles:
    try:
        user = api.get_user(handle)
        name = user.name
        print("User: " + name + ", Twitter handle: " + handle)
        tweets_count = user.statuses_count
        print("Tweets: " + str(tweets_count))
        friends_count = user.friends_count
        print("Following: " + str(friends_count))
        followers_count = user.followers_count
        print("Followers: " + str(followers_count))
        statuses = api.user_timeline(screen_name=handle, exclude_replies=True, tweet_mode="extended")
        print("Number of statuses fetched: " + str(len(statuses)))
        # tweepy.Cursor(api.user_timeline, screen_name=handle, exclude_replies=True).items(200)
        for status in statuses:
            author = ""
            original_or_retweet = ""
            message = ""
            favorite_count = ""
            if hasattr(status, 'retweeted_status'):
                author = status.retweeted_status.user.name
                message = status.retweeted_status.full_text
                favorite_count = status.retweeted_status.favorite_count
                original_or_retweet = "Retweeted"
            else:
                author = user.name
                message = status.full_text
                favorite_count = status.favorite_count
                original_or_retweet = "Original"
            print("Initial tweet by: " + author)
            print(message)
            message_id = status.id_str
            print(message_id)
            created_at = status.created_at
            print("Date and time: " + str(created_at))
            retweet_count = status.retweet_count
            print("Number of retweets: " + str(retweet_count))
            print("Number of likes: " + str(favorite_count))
            print("Original/Retweet = " + original_or_retweet)
            sql = "REPLACE INTO twitter_import$stream (NAME, HANDLE, NO_OF_TWEETS, FOLLOWING, FOLLOWERS, INITIAL_TWEET_BY, MESSAGE, MESSAGE_ID, DATETIME, NO_OF_RETWEETS, NO_OF_LIKES, ORIGINAL_OR_RETWEET) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (name, handle, str(tweets_count), str(friends_count), str(followers_count), author, message, message_id, created_at, str(retweet_count), str(favorite_count), original_or_retweet)
            mycursor.execute(sql, val)
            mydb.commit()
    except tweepy.TweepError:
        pass
