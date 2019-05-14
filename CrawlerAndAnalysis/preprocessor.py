#----------------------------------------------------------#
# Program: preprocessor.py
# Purpuose: A script to preprocess tweets text and location
# Group Member:
#          Victor Ding 1000272
#          Zhuolin He 965346
#          Chenyao Wang 928359
#          Danyang Wang 963747
#          Yuming Zhang 973693
#----------------------------------------------------------#

import nlp
import json

def preprocessor(data):
    
    regions = ["New South Wales", "Victoria", "Queensland", "Western Australia", "South Australia", 
               "Tasmania", "Northern Territory", "Australian Capital Territory"]
    
    # Process Text
    processed = nlp.ProcessText(data["text"])
    processed["location"] = None

    # Process Location
    for region in regions:
        if region.lower() in data["place"]["full_name"].lower():
            processed["location"] = region
        
    #if processed["location"] == None:
    #    print('Location not found! Place of tweet is:',data["place"]["full_name"].lower())
    
    return processed
