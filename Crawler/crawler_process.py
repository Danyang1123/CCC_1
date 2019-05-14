#------------------------------------------------------------#
# Program: crawler.py
# Purpuose: A script to search and save tweets with options
#           and process the tweet and store in couchDB
# Group Member:
#          Victor Ding 1000272
#          Zhuolin He 965346
#          Chenyao Wang 928359
#          Danyang Wang 963747
#          Yuming Zhang 973693
#------------------------------------------------------------#

# Import Packages
import json
import tweepy
import datetime
import time
import math
import couchdb
from launch_api import launch_api
import preprocessor

# search and save tweets
def search_n_save(query='*',
	              geocode="-27.782292,133.793118,2104.3km",
	              until=datetime.datetime.today().strftime('%Y-%m-%d'),
	              result_type='recent',
	              ntweet=300,
	              max_turn=100,
	              host='http://********:********@172.26.37.201:5984',
	              dataset=None,
	              max_id=None,
	              since_id=None):

	# Create CouchDB Dataset if not given/exist
	if dataset == None:
		time_now = str(datetime.datetime.now().time())[0:5]
		dataset = 'au_pro_' + str(until) + '_' + time_now.replace(':','_')
	
	couch = couchdb.Server(host)
	if dataset in couch:
		db = couch[dataset]
	else:
		db = couch.create(dataset)

	# Settings Massages
	print('Search_and_Save running in the following settings:')
	print('query=',query)
	print('geocode=',geocode)
	print('until=',until)
	print('result_type=',result_type)
	print('Max turn:',max_turn,', for each turn',ntweet,'will be retrived.')
	print('Storing in',host,'in dataset:',dataset)
	back_up_since = None
	if since_id:
		back_up_since = since_id
		print('We are grabbing tweets from id:', back_up_since)

	# API ID and Initial API
	api_id = 0
	api, api_num, max_app_id = launch_api(api_id)

	# Create a clock to record the start time of each app
	start_clock = [None]*(max_app_id+1)
	start_clock[api_num] = time.time()

	# Define Turn to indicate how many times requests are made
	turn = 0

	# Define a counter for total tweets
	total_count = 0
 
	# Define max_id_run
	max_id_run=None

	# First Tweet
	ftweet = True

	# Loop Until Conditions Meet
	# if since_id exist, keep running until break; if not depends on max_turn
	while turn < max_turn or since_id: 

		# Temporary Container per turn
		tweet_list = []

		# Update Turn
		turn += 1
		
		# Try search tweets with options
		try:
			# If max_id is not given
			if max_id == None:
				for tweet in tweepy.Cursor(api.search,
					q=query,
					geocode=geocode,
					until=until,
					result_type=result_type,
					lang='en').items(ntweet):

					# Store the first id we looked in this run
					if ftweet:
						max_id_run = tweet.id
						print('The first ID we are looking at is:', max_id_run)
						ftweet = False
				
					# If since_id is reached
					if since_id and tweet.id <= since_id:
						print('Hit bottom!')
						turn = max_turn
						since_id = None
						break

					# Calculate the next max_id
					max_id = str(tweet.id-1)

					# Sotre all tweets in a list
					tweet_list.append(tweet._json)

			# If max_id is given
			else:
				for tweet in tweepy.Cursor(api.search,
					q=query,
					geocode=geocode,
					until=until,
					result_type=result_type,
					lang='en',
					max_id = max_id).items(ntweet):

					# Store the first id we looked in this run
					if ftweet:
						max_id_run = tweet.id
						print('The first ID we are looking at is:', max_id_run)
						ftweet = False

					# If since_id is reached
					if since_id and tweet.id <= since_id:
						print('Hit bottom!')
						turn = max_turn
						since_id = None
						break
				
					# Calculate the next max_id
					max_id = str(tweet.id-1)

					# Store all tweets in a list
					tweet_list.append(tweet._json)

			# If there are new tweets
			if tweet_list != []:
				# Save to DB
				count = 0
				for tweet in tweet_list:
					if tweet['place']:
						try:
							# Process Tweet
							processed = preprocessor.preprocessor(tweet)
							processed['id'] = tweet['id']
							# See if Tweet has location
							if processed['location'] == None:
								continue
							else:
								db.save(processed)
								count+=1

						except couchdb.http.ResourceConflict:
							print("Duplicate tweets found and ingnored.")
	
				print('Turn',turn,'ends! Totally',count,'tweets are loaded. Next Max ID:',max_id)

				# Keep count of all tweets stored in this run
				total_count += count
			
			# Step the program if no new tweets
			else:
				turn = max_turn
				since_id = None

			# If last turn, output a log file
			if turn == max_turn:
				last_id_run = int(max_id)+1

				log_file = 'run-' + dataset + '.log'

				string1 = 'The first id we looked is ' + str(max_id_run) + "\n"
				string2 = 'The last id we looked is '+ str(last_id_run) + "\n"
				string3 = 'Totally ' + str(total_count) + ' tweets were stored in ' + dataset + ' dataset.' + "\n"

				with open(log_file,'w',encoding='utf-8') as log:
					print('Search_and_Save run in the following settings:',file=log)
					print('query=',query,file=log)
					print('geocode=',geocode,file=log)
					print('until=',until,file=log)
					print('result_type=',result_type,file=log)
					print('Storing in',host,'in dataset:',dataset,file=log)
					if back_up_since:
						print('We are grabbing tweets from id:', back_up_since)
					print('',file=log)
					log.write(string1)
					log.write(string2)
					log.write(string3)
				
		# If rate limit is hit, switch to the next app
		except tweepy.error.TweepError as e:

			# Messages
			print(e)
			print('#',api_num,' API app hits rate limit(or other error), switching to next app.')

			# Reduce Turn by 1 when rate limit hits
			turn -= 1

			# Switch to the next app
			api_id += 1
			api, api_num, max_app_id = launch_api(api_id)

			# Check if the app ever used
			if start_clock[(api_num)] == None:

				# Mark Start Time
				start_clock[api_num] = time.time()
				print('switched to #',api_num,'app!')
				continue

			# If it's used before, we may need to wait
			else:
				# Calculate Wait time on next app
				wait_time = 900 - math.floor(time.time() - start_clock[api_num])

				# If we need to wait
				if wait_time > 0:
					print('Next app in rest, wait for',wait_time,'seconds...')
					time.sleep(wait_time)
				
				# New start time
				start_clock[api_num] = time.time()

				print('switched to #',api_num,'app!')
				continue

# Change options to run the program for specific purpose
# search_n_save(host='http://admin:****:****@172.26.37.250:5984',
#	          max_turn=100000,since_id=1127000363624611842)
