ReadMe

1. nlp.py
- Dependency: None
- Purpose: Perform sentiment analysis on the text from the tweets fed to this program.

2. preprocessor.py
- Dependency: nlp.py
- Purpose: Perform sentiment analysis from nlp.py as well as finding the location of the tweet fed.

3. launch_api.py	
- Dependency: None
- Purpose: Create App-Authorise REST Search API using build-in consumber key(s) and secret(s)

4. crawler_process.py	
- Dependency: nlp.py, preprocessor.py, launch_api.py and user specified parameters	
- Purpose:
  1. Request tweets from Twitter using specified parameters.
  2. Process tweets using methods in nlp.py and preprocessor.py.
  3. Store processed tweets in CouchDB
