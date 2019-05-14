#-----------------------------------------------------------#
# Program: lauch_api.py
# Purpuose: A script to lauch twitter developer api
# Group Member:
#          Victor Ding 1000272
#          Zhuolin He 965346
#          Chenyao Wang 928359
#          Danyang Wang 963747
#          Yuming Zhang 973693
#-----------------------------------------------------------#

import tweepy
from tweepy import OAuthHandler

# App Laucher
def launch_api(api_id):

	# Consumer Keys
	consumer_key = ['*************************',
	                '*************************',
	                '*************************',
	                '*************************',
	                '*************************']

    # Consumer Secrets
	consumer_secret = ['**************************************************',
	                   '**************************************************',
	                   '**************************************************',
	                   '**************************************************',
	                   '**************************************************']

	# Calculate API Num
	api_num = api_id % len(consumer_key)

	# max app id
	max_app_id = len(consumer_key)-1

	# Authorize
	auth = OAuthHandler(consumer_key[api_num], consumer_secret[api_num])

	# Api
	api = tweepy.API(auth,wait_on_rate_limit=False,wait_on_rate_limit_notify=True)

	return [api,api_num,max_app_id]
