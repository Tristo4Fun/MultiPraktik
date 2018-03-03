import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import re
#initialising Twitter user
#id and secret
auth = tweepy.OAuthHandler('bCZwVzklnlD74MUvsFDz0oFo2', 'qAmYYrV3MVqadWBMbW73eZ8e4Z5infJ62dLytzV1fZMoLAkKb4')
#access token id, access token secret
auth.set_access_token('409511921-C0fLT44yBcyl4GpRqwzEuyXnn84LJaYafcYLBG7M', 'KJ0wEMeuUSNBxNlpNi5Nb7ZLYn0KTDp01KosKRi1M9Dtq')
api = tweepy.API(auth)
#steam_tweets = api.user_timeline('steam_games')
# for tweet in steam_tweets:
# 	print(tweet.text)

class StdOutListener(StreamListener):
	""" A listener handles tweets that are received from the stream."""
	def on_status(self, status):
		if re.search('deal',status.text,re.IGNORECASE):
			with open('twitter.txt', 'w') as f:
				f.write(status.text)
		return True

	def on_error(self, status):
		print(status)

stream = Stream(auth, StdOutListener())
stream.userstream('steam_games')
stream.filter(track=['#SteamDailyDeal','#MidweekMadness'])
print('Twitter ready')

