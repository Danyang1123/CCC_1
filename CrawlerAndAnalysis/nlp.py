#-----------------------------------------------------------#
# Program: nlp.py
# Purpuose: A script to preprocess tweets text
# Group Member:
#          Victor Ding 1000272
#          Zhuolin He 965346
#          Chenyao Wang 928359
#          Danyang Wang 963747
#          Yuming Zhang 973693
#-----------------------------------------------------------#

import nltk, nltk.sentiment.vader
import spacy

nltk.download('vader_lexicon')
SentimentIntensityAnalyzer = nltk.sentiment.vader.SentimentIntensityAnalyzer()
nlp = spacy.load('en_core_web_md')
keywords = ["pride", "greed", "lust", "envy", "gluttony", "wrath", "sloth"]
kwnlp    = [nlp(keyword) for keyword in keywords]

def ProcessText(text):
    results = dict(zip(keywords, [_.similarity(nlp(text)) for _ in kwnlp]))
    # Append sentiment score
    results["sentiment"] = SentimentIntensityAnalyzer.polarity_scores(text)["compound"]
    return results
