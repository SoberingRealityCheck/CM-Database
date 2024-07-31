WEBSITE!
-
Requirements to run:
-
```
python            3.9.18
Django            4.0.10
djongo            [1.3.6](https://github.com/bslocombe/djongo/tree/master)
pymongo           3.12.1
pytz              2022.2.1
sqlparse          0.4.2
```

Current status:
-
Accessing sql database & statics works while settings.py is set to ```Debug=True``` and the server is run via ```python .../CM-Database/manage.py runserver```.

```Debug=False``` and ```systemctl start httpd``` passes that functionality to the Apache service. This only works when run on HEP11 as it is the only machine configured to work properly with our code (for now).

IMPORTANT:
-
Along with the code in this repo there is also a 21.6 GB 'media' folder that contains several different sorts of files related to the old QIE database. And a great photo of an anteater. I can't tell what is accessing it.

If you run into issues and need to scp that to your local device, the directory is located on hep01 under the filepath ```/hep01-data1/hep06-copy/django/testing_database_he/media```.

Should be placed next to your github repo folder in a folder named 'QIE_media' for the program to locate it. 

Not including it in the github repo because github did not like it when i tried to push a 86,000 file commit... 


Starting the server:
-
Open a terminal window. Run ```mongod``` to start the mongoDB server.
In a seperate terminal window, run ```sudo systemctl start httpd``` to start Apache.
visiting ```http://hep11/hgcal/cm``` in a browser window should now display the Django homepage.

Interacting with the MongoDB Server:
-
If you want to interact directly with the server, open a seperate window and use ```mongosh``` to start a mongoDB shell.
```use db``` will put you into the CM database, and ```show collections``` will show you the currently stored variables. 
```var myCursor = db.cm_db_cm_test_result.find()``` creates a cursor that you can inspect with ```myCursor``` to read the stored data. 

Debugging:
-
Apache error log is located in the default spot, under ```/etc/httpd/logs/error_log```. You may not be able to access the folder but you can read the file directly with sudo. 
