WEBSITE!
-
Requirements to run:
-
- Python 3.11.x
- Django 5.x

Current status:
-
Accessing sql database & statics works while settings.py is set to ```Debug=True```.

```Debug=False``` passes that functionality to Apache, which is currently not implemented because I have no clue how to use it. That is a problem for next week...

IMPORTANT:
-
Along with the code in this repo there is also a 21.6 GB 'media' folder that contains... images of the chips, i think? I can't tell what is accessing it.

If you run into issues and need to scp that to your local device, the directory is located on hep01 under the filepath ```/hep01-data1/hep06-copy/django/testing_database_he/media```.

Should be placed next to your github repo folder in a folder named 'QIE_media' for the program to locate it. 

Not including it in the github repo because github did not like it when i tried to push a 86,000 file commit... 
