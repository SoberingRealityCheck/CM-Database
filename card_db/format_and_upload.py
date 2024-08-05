#!/usr/bin/env python
# coding: utf-8

# In[ ]:

#this script was originally written by Alex Campbell for use on the ECON-T tests: https://github.com/SC990987/MongoDBScripts 
#I have modified it to upload via django instead of pymongo - it also now splits the data into seperate 'card' and 'test' documents for faster retrieval of commonly accessed 'summary' variables

import numpy as np
import glob
import json
import djongo 
from cm_db.models import CM_Card, Test
from traceback_with_variables import activate_by_import
import os

## Grab JSON Files
idir = "/data/www/html/django/CM-Database/imports"
odir = "/data/www/html/django/CM-Database/media/logs"
a = f"{idir}/report*.json"
fnames = list(np.sort(glob.glob(f"{idir}/report*.json")))
import traceback

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

def get_Barcode(data):
    null_chip_ID = "MissingID"
    if 'chip_number' in data and data['chip_number']: 
        barcode = data['chip_number']
    else: 
        barcode = null_chip_ID
    return barcode

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
    newcard.barcode = get_Barcode(data)
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
    for test in test_outcomes:
        date = fname[62:][:10]
        test["most_recent_date"] = date
    newcard.test_outcomes = test_outcomes
    #save test details
    newcard.save()

def Update_Existing_Card(data, fname):
    barcode = get_Barcode(data)
    oldcard = CM_Card.objects.filter(barcode = barcode)[0]
    #id assignment is easy. Just leave it as is
    old_test_outcomes = oldcard.test_outcomes
    test_outcomes = []
    for test in data['tests']:
        test_name = f"{stringReplace(test['nodeid'].split('::')[1])}"
        result = selector(test['outcome'])
        new = True
        #nesting a for loop here is very slow. There's likely a clever workaround using faster pymongo querying but for now this is a temporary solution.
        for test in old_test_outcomes:
            if test["test_name"] == test_name:
                new = False
                test_outcome_new = test
                test_outcome_new["total"] = str(int(test_outcome_new["total"])+1)
                if result == 1:
                    test_outcome_new["passed"] = str(int(test_outcome_new["passed"])+1)
                    if test["passed"] == test["total"]:
                        test_outcome_new["result"] = "Passed"
                elif result == 0:
                    if test["anyForced"] != 1:
                        test_outcome_new["result"] = "Failed"
                    test_outcome_new["anyFailed"] = 1
                    test_outcome_new["failed"] = str(int(test_outcome_new["failed"])+1)
                    #print(test_outcome_new["failed"])
                elif result == -1:
                    if test["passed"] != test["total"]:
                        test_outcome_new["result"] = "Incomplete"
                    #test_outcome_new["result"] = "Forced"
                    #test_outcome_new["anyForced"] = 1
                test_outcomes.append(test_outcome_new)
                pass
        if new:
            test_outcome_new = {"test_name":test_name, "passed":0, "total":1, "failed":0, "anyForced":0, "anyFailed":0, "result":"Incomplete"}
            if result == 1:
                test_outcome_new["passed"] = 1
                test_outcome_new["result"] = "Passed"
            elif result == 0:
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
        elif result == "Forced":
            test["get_css_class"] = "forced"
        elif result == "Failed":
            test["get_css_class"] = "bad"
        elif result == "Incomplete":
            test["get_css_class"] = "warn"


    #TEMP BANDAID FIX BECAUSE I DO NOT YET KNOW WHICH TESTS ARE REQUIRED
    for test in test_outcomes:
        test["required"] = 1
    for test in test_outcomes:
        date = fname[62:][:10]
        test["most_recent_date"] = date
    oldcard.test_outcomes = test_outcomes
    #save test details
    
    oldcard.save()


def UploadTests(data, fname):
    barcode = get_Barcode(data)
    for i, test in enumerate(data['tests']):
        new_test = Test.objects.create()
        new_test.test_name = f"{stringReplace(test['nodeid'].split('::')[1])}"
        new_test.barcode = barcode
        date = str(fname[62:][:10])
        hour = int(fname[73:][:2])
        minute = str(int(fname[76:][:2]))
        if minute == '0':
            minute = '00'
        if hour > 12:
            time = date + ": " + str(hour % 12) + ":" + minute + " PM"
        else:
            time = date + ": " + str(hour) + ":" + minute + " AM"
        new_test.date_run = time
        new_test.outcome = test['outcome']
        if 'metadata' in test:
            #print(test['metadata'])
            if "eRX_errcounts" in test['metadata']:
                new_test.eRX_errcounts = Metadata_Formatter(test['metadata'], "eRX_errcounts")
            else:
                new_test.eRX_errcounts = None
            if "eTX_errcounts" in test['metadata']:
                new_test.eTX_errcounts = Metadata_Formatter(test['metadata'], "eTX_errcounts")
            else:
                new_test.eTX_errcounts = None
            if "eTX_bitcounts" in test['metadata']:
                new_test.eTX_bitcounts = Metadata_Formatter(test['metadata'], "eTX_bitcounts")
            else:
                new_test.eTX_bitcounts = None
            if "eTX_delays" in test['metadata']:
                new_test.eTX_delays = Metadata_Formatter(test['metadata'], "eTX_delays")
            else:
                new_test.eTX_delays = None
            new_test.failure_information = {
                "failure_mode": test['call']['traceback'][0]['message'] if 'traceback' in test['call'] and test['call']['traceback'][0]['message'] != '' else test['call']['crash']['message'],
                "failure_cause": test['call']['crash']['message'],
                "failure_code_line": test["call"]["crash"]["lineno"],
            } if 'failed' in test['outcome'] else None
        #save test metadata
        new_test.branch = data['branch']
        new_test.commit_hash = data['commit_hash']
        new_test.remote_url = data['remote_url']
        new_test.status = data['status']
        new_test.firmware_name = data['firmware_name']
        new_test.firmware_git_desc = data['firmware_git_desc']
        new_test.filename = fname
        
        new_test.save()
    print(i+1,"tests added to file of chip",barcode)

def jsonFileUploader(fname):
    ## open the JSON File
    with open(fname) as jsonfile:
        data = json.load(jsonfile)
    ## preprocess the JSON file
    barcode = get_Barcode(data)
    #check DB for existing entries of the same name. Decide whether to update existing entry or create new one
    ID_List = CM_Card.objects.values_list('barcode',flat=True)
    #print(ID_List)
    if barcode in ID_List:
        print(barcode, "already exists! Updating Entry with new data...")
        Update_Existing_Card(data, fname)
    else:
        print(barcode, "not listed in database! Creating new entry...")
        Create_Fresh_Card(data, fname)
    
    UploadTests(data, fname)
## upload all the JSON files in the database

def main():
    print("starting file upload script...")
    filename_list = list(Test.objects.values_list("filename"))
    #print("FILENAME LIST:",filename_list)
    num_uploads = 0
    for i, (fname) in enumerate(fnames):
        if (fname,) not in filename_list:
            print("uploading file",i)
            jsonFileUploader(fname)
            #this is to prevent accidentally uploading two of the same file at once
            filename_list.append(fname)
            num_uploads += 1
        else: print ("file already uploaded! skipping.")
        fname = fname[50:]
        print(fname)
        os.rename(f"{idir}/{fname}", f"{odir}/{fname}")
    if num_uploads != 0: print("Script complete.", num_uploads,"files uploaded.")
    else: 
        print("Script complete, but 0 files uploaded. Perhaps double-check the files are in the specified import directory?")
        print("IDIR:", idir)
if __name__=="__main__": 
    main()
