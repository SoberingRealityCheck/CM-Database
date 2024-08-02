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

def Metadata_Formatter(metadata, metadata_type):
    #print("formatting metadata of type", metadata_type)
    if metadata_type in ["eRX_errcounts", "eTX_errcounts", "eTX_bitcounts", "eTX_delays"]:
        #print("metadata type approved!")
        if metadata_type in metadata:
            #print("metadata located in input!")
            old_list = metadata[metadata_type]
            labeled_list = []
            nested = any(isinstance(sub, list) for sub in old_list)
            if nested:
                for row in old_list:
                    #print("row:",row)
                    rowdict = {}
                    for i, value in enumerate(row):
                        rowdict[f'{metadata_type[:3]}{i+1}'] = row[i]
                    #print("rowdict:",rowdict)
                    labeled_list.append(rowdict)
                #print("metadata output:",labeled_list)
                return labeled_list
            else:
                #print("row:",old_list)
                rowdict = {}
                for i, value in enumerate(old_list):
                    rowdict[f'{metadata_type[:3]}{i+1}'] = old_list[i]
                #print("rowdict:",rowdict)
                labeled_list.append(rowdict)
                #print("metadata output:",labeled_list)
                return labeled_list
        else:
            return
    else:
        print("ERROR! metadata type", metadata_type, "unknown.")

def Create_Fresh_Card(data, fname):
    newcard = CM_Card.objects.create()
    if 'chip_number' in data and data['chip_number']: 
        newcard.identifier = data['chip_number']
    else: 
        newcard.identifier = "NO_ID"
    #save test outcomes
    test_outcomes = []
    for test in data['tests']:
        test_outcome_temp = {"test_name":f"{stringReplace(test['nodeid'].split('::')[1])}", "passed":0, "total":1, "failed":0, "anyFailed":0, "anyForced":0, "result":"Incomplete"}
        result = selector(test['outcome'])
        if result == 1:
            test_outcome_temp['passed'] = 1
            test_outcome_temp["result"] = "Passed"
        if result == 0:
            test_outcome_temp["result"] = "Failed"
            test_outcome_temp["anyFailed"] = 1
            test_outcome_temp["failed"] = 1
        #if result == -1:
            #test_outcome_temp["result"] = "Forced"
            #test_outcome_temp["anyForced"] = 1
        test_outcomes.append(test_outcome_temp)
    for test in test_outcomes:
        result = test["result"]
        if result == "Passed":
            test["get_css_class"] = "okay"
        if result == "Forced":
            test["get_css_class"] = "forced"
        if result == "Failed":
            test["get_css_class"] = "bad"
        if result == "Incomplete":
            test["get_css_class"] = "warn"
    #TEMP BANDAID FIX BECAUSE I DO NOT YET KNOW WHICH TESTS ARE REQUIRED
    for test in test_outcomes:
        test["required"] = 1
    newcard.test_outcomes = test_outcomes
    #save test details
    test_details = []
    for test in data['tests']:
        metadata = {}
        if 'metadata' in test:
            #print(test['metadata'])
            if "eRX_errcounts" in test['metadata']:
                metadata["eRX_errcounts"] = Metadata_Formatter(test['metadata'], "eRX_errcounts")
            else:
                metadata["eRX_errcounts"] = None
            if "eTX_errcounts" in test['metadata']:
                metadata["eTX_errcounts"] = Metadata_Formatter(test['metadata'], "eTX_errcounts")
            else:
                metadata["eTX_errcounts"] = None
            if "eTX_bitcounts" in test['metadata']:
                metadata["eTX_bitcounts"] = Metadata_Formatter(test['metadata'], "eTX_bitcounts")
            else:
                metadata["eTX_bitcounts"] = None
            if "eTX_delays" in test['metadata']:
                metadata["eTX_delays"] = Metadata_Formatter(test['metadata'], "eTX_delays")
            else:
                metadata["eTX_delays"] = None
        test_details_temp = {
                "test_name":f"{stringReplace(test['nodeid'].split('::')[1])}", 
                "test_metadata": metadata if metadata!={} else None,
                "failure_information":{
                    "failure_mode": test['call']['traceback'][0]['message'] if 'traceback' in test['call'] and test['call']['traceback'][0]['message'] != '' else test['call']['crash']['message'],
                    "failure_cause": test['call']['crash']['message'],
                    "failure_code_line": test["call"]["crash"]["lineno"],
                } if 'failed' in test['outcome'] else None
                }
        test_details.append(test_details_temp)
    if test_details != []:
        newcard.test_details = test_details 
    #save test metadata
    newcard.card_metadata = [{
        "branch": data['branch'],
        "commit_hash": data['commit_hash'],
        "remote_url": data['remote_url'],
        "status": data['status'],
        "firmware_name": data['firmware_name'],
        "firmware_git_desc": data['firmware_git_desc'],
        "filename": fname
        }]

    newcard.save()

def Update_Existing_Card(data, fname):
    if 'chip_number' in data and data['chip_number']: 
        identifier = data['chip_number']
    else: 
        identifier = "NO_ID"
    oldcard = CM_Card.objects.filter(identifier = identifier)[0]
    #id assignment is easy. Just leave it as is
    test_outcomes = oldcard.test_outcomes
    for test in data['tests']:
        test_name = f"{stringReplace(test['nodeid'].split('::')[1])}"
        result = selector(test['outcome'])
        new = True
        for test in test_outcomes:
            if test["test_name"] == test_name:
                new = False
                test_outcome_new = test
                test_outcome_new["total"] = str(int(test_outcome_new["total"])+1)
                if result == 1:
                    test_outcome_new["passed"] = str(int(test_outcome_new["passed"])+1)
                    if test["anyForced"] == 0:
                        test_outcome_new["result"] = "Passed"
                if result == 0:
                    if test["anyForced"] == 0:
                        test_outcome_new["result"] = "Failed"
                    test_outcome_new["anyFailed"] = 1
                    test_outcome_new["failed"] = str(int(test_outcome_new["failed"])+1)
                    #print(test_outcome_new["failed"])
                #if result == -1:
                    #test_outcome_new["result"] = "Forced"
                    #test_outcome_new["anyForced"] = 1
                test = test_outcome_new
                pass
        if new:
            test_outcome_new = {"test_name":test_name, "passed":0, "total":1, "failed":0, "anyForced":0, "anyFailed":0, "result":"Incomplete"}
            if result == 1:
                test_outcome_new["passed"] = 1
                test_outcome_new["result"] = "Passed"
            if result == 0:
                test_outcome_new["result"] = "Failed"
                test_outcome_new["anyFailed"] = 1
                test_outcome_new["failed"] = 1
            #if result == -1:
                #test_outcome_new["result"] = "Forced"
                #test_outcome_new["anyForced"] = 1
            test_outcomes.append(test_outcome_new)
    for test in test_outcomes:
        result = test["result"]
        if result == "Passed":
            test["get_css_class"] = "okay"
        if result == "Forced":
            test["get_css_class"] = "forced"
        if result == "Failed":
            test["get_css_class"] = "bad"
        if result == "Incomplete":
            test["get_css_class"] = "warn"


    #TEMP BANDAID FIX BECAUSE I DO NOT YET KNOW WHICH TESTS ARE REQUIRED
    for test in test_outcomes:
        test["required"] = 1
    oldcard.test_outcomes = test_outcomes
    #save test details
    test_details = oldcard.test_details
    for test in data['tests']:
        metadata = {}
        if 'metadata' in test:
            #print(test['metadata'])
            if "eRX_errcounts" in test['metadata']:
                metadata["eRX_errcounts"] = Metadata_Formatter(test['metadata'], "eRX_errcounts")
            else:
                metadata["eRX_errcounts"] = None
            if "eTX_errcounts" in test['metadata']:
                metadata["eTX_errcounts"] = Metadata_Formatter(test['metadata'], "eTX_errcounts")
            else:
                metadata["eTX_errcounts"] = None
            if "eTX_bitcounts" in test['metadata']:
                metadata["eTX_bitcounts"] = Metadata_Formatter(test['metadata'], "eTX_bitcounts")
            else:
                metadata["eTX_bitcounts"] = None
            if "eTX_delays" in test['metadata']:
                metadata["eTX_delays"] = Metadata_Formatter(test['metadata'], "eTX_delays")
            else:
                metadata["eTX_delays"] = None
        test_details_temp = {
                "test_name":f"{stringReplace(test['nodeid'].split('::')[1])}", 
                "test_metadata": metadata if metadata!={} else None,
                "failure_information":{
                    "failure_mode": test['call']['traceback'][0]['message'] if 'traceback' in test['call'] and test['call']['traceback'][0]['message'] != '' else test['call']['crash']['message'],
                    "failure_cause": test['call']['crash']['message'],
                    "failure_code_line": test["call"]["crash"]["lineno"],
                } if 'failed' in test['outcome'] else None
                }
        test_details.append(test_details_temp)
    if test_details != []:
        oldcard.test_details = test_details 
    #save test metadata
    metadata = oldcard.card_metadata
    new_metadata = {
        "branch": data['branch'],
        "commit_hash": data['commit_hash'],
        "remote_url": data['remote_url'],
        "status": data['status'],
        "firmware_name": data['firmware_name'],
        "firmware_git_desc": data['firmware_git_desc'],
        "filename": fname
        }
    metadata.append(new_metadata)

    oldcard.save()

def jsonFileUploader(fname):
    ## open the JSON File
    with open(fname) as jsonfile:
        data = json.load(jsonfile)
    ## preprocess the JSON file
    if 'chip_number' in data and data['chip_number']: 
        identifier = data['chip_number']
    else: 
        identifier = "NO_ID"
    #check DB for existing entries of the same name. Decide whether to update existing entry or create new one
    ID_List = CM_Card.objects.values_list('identifier',flat=True)
    #print(ID_List)
    if identifier in ID_List:
        print(identifier, "already exists! Updating Entry with new data...")
        Update_Existing_Card(data, fname)
    else:
        print(identifier, "not listed in database! Creating new entry...")
        Create_Fresh_Card(data, fname)
    '''
    newcard.summary = {
            "passed":data['summary']['passed'] if 'passed' in data['summary'] else 0, 
            "error":data['summary']['error'] if 'error' in data['summary'] else 0,
            "total":data['summary']['total'] if 'total' in data['summary'] else 0,
            "collected": data['summary']['collected'] if 'collected' in data['summary'] else 0
            }
    '''
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
## upload all the JSON files in the database

def main():
    filename_list = []
    metadata_list = CM_Card.objects.values_list("card_metadata")
    for entry in metadata_list:
        print("entry:", entry)
        if entry:
            if entry[0]:
                for metadata_array in entry:
                    for metadata in metadata_array:
                        print("metadata:",metadata)
                        filename_list.append(metadata["filename"])
    print("FILENAME LIST:",filename_list)
    for i, (fname) in enumerate(fnames):
        if fname not in filename_list:
            print("uploading file",i)
            jsonFileUploader(fname)
            #this is to prevent accidentally uploading two of the same file at once
            filename_list.append(fname)
        else: print ("file already uploaded! skipping.")

if __name__=="__main__": 
    main()
