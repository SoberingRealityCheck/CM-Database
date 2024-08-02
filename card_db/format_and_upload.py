#!/usr/bin/env python
# coding: utf-8

# In[ ]:

#this script was originally written by Alex Campbell for use on the ECON-T tests: https://github.com/SC990987/MongoDBScripts 
#I have slightly modified it to create a seperate 'summaries' database in addition to its previous functionality - this enables faster querying 

import numpy as np
import glob
import json
import djongo 
from cm_db.models import CM_Card
from traceback_with_variables import activate_by_import

## Grab JSON Files
idir = "/data/www/html/django/CM-Database/card_db/imports"
a = f"{idir}/report*.json"
fnames = list(np.sort(glob.glob(f"{idir}/report*.json")))
import traceback
'''
## Connect to a local Database
client = pymongo.MongoClient("mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.2.12") # Connect to local database
session = client.start_session()


mydatabase = client['db'] # create new database
mycol = mydatabase['cm_db_cm_test_result']
fastcol = mydatabase['cm_db_cmsummary']
'''
def selector(input):
    if input == 'passed':
        return 1
    elif input == 'failed':
        return 0
    ## This is for a test that was skipped
    else:
        return -1

def stringReplace(word):
    if "[" in word:
        word = word.replace("[","_")
    if ".." in word:
        word = word.replace("..","_")
    if "/" in word:
        word = word.replace("/","_")
    if "]" in word:
        word = word.replace("]", "")
    return word

def jsonFileUploader(fname):
    ## open the JSON File
    with open(fname) as jsonfile:
        data = json.load(jsonfile)
    ## preprocess the JSON file
    try:
        newcard = CM_Card.objects.create()
    except:
        print("ERROR: issue fetching models.py CM_Card object.")
    try:
        if 'chip_number' in data and data['chip_number']: 
            newcard.identifier = data['chip_number']
            newcard.save()
        else: 
            newcard.identifier = "NO_ID"
    except:
        print("ERROR: ID Assignment in", fname)
    try:
        newcard.summary = {"passed":data['summary']['passed'], "total":data['summary']['total'], "collected": data['summary']['collected']}
        newcard.save()
    except:
        print("ERROR: summary creation in", fname)
    try:
        test_outcomes = []
        for test in data['tests']:
            test_outcome_temp = {"test_name":f"{stringReplace(test['nodeid'].split('::')[1])}",
                    "test_result":selector(test['outcome'])}
            test_outcomes.append(test_outcome_temp)
        newcard.test_outcomes = test_outcomes
        newcard.save()
    except:
        print("ERROR: Test Outcome Creation in", fname)
    try:
        test_details = []
        for test in data['tests']:
            test_details_temp = {
                    "test_name":f"{stringReplace(test['nodeid'].split('::')[1])}", 
                    "test_metadata": test['metadata'] if 'metadata' in test else None,
                    "failure_information":{
                        "failure_mode": test['call']['traceback'][0]['message'] if test['call']['traceback'][0]['message'] != '' else test['call']['crash']['message'],
                        "failure_cause": test['call']['crash']['message'],
                        "failure_code_line": test["call"]["crash"]["lineno"],
                    } if 'failed' in test['outcome'] else None
                    }
            test_details.append(test_details_temp)
        newcard.test_details = test_details 
        newcard.save()
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        print("ERROR: Test Details Creation in", fname)
    try:
        newcard.card_metadata = {
            "branch": data['branch'],
            "commit_hash": data['commit_hash'],
            "remote_url": data['remote_url'],
            "status": data['status'],
            "firmware_name": data['firmware_name'],
            "firmware_git_desc": data['firmware_git_desc'],
            "filename": fname
            }
        newcard.save()
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        print("ERROR: Card Metadata Creation in", fname)
    '''
    newcard.card_metadata.branch = data['branch']
    newcard.card_metadata.commit_hash = data['commit_hash']
    newcard.card_metadata.remote_url = data['remote_url']
    newcard.card_metadata.status = data['status']
    newcard.card_metadata.firmware_name = data['firmware_name']
    newcard.card_metadata.firmware_git_desc = data['firmware_git_desc']
    newcard.card_metadata.filename = fname
    '''
    '''
    dict2 = {
            "summary": {'passed': data['summary']['passed'], 'total':data['summary']['total'], 'collected':data['summary']['collected']},
            "individual_test_outcomes": {
                f"{stringReplace(test['nodeid'].split('::')[1])}": selector(test['outcome']) for test in data['tests']
            },
            "identifier": data['chip_number']
            }
    '''
    ## Insert File into the DB 
    try:
        newcard.save()
        print(fname, "uploaded successfully.")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        print("ERROR: Django Model Save of", fname)
## upload all the JSON files in the database

def main():
    for i, (fname) in enumerate(fnames):
        try:
            jsonFileUploader(fname)
        except Exception as e:
            print(e, fname, i)
            traceback.print_tb(e.__traceback__)

if __name__=="__main__": 
    main()
