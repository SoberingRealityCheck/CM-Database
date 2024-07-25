WEBSITE!
-
Requirements to run:
-
- Python 3.11.x
- Django 5.x

currently looking at using a different environment for our mongodb compatibility with:

```
sgiref           3.8.1
bson              0.5.8
dataclasses       0.6
Django            4.0.10
djongo            [1.3.6](https://github.com/bslocombe/djongo/tree/master)
pip               24.1.2
pymongo           3.12.1
python-dateutil   2.9.0.post0
pytz              2022.2.1
setuptools        70.1.1
six               1.16.0
sqlparse          0.4.2
typing_extensions 4.12.2
wheel             0.43.0
```

Current status:
-
Accessing sql database & statics works while settings.py is set to ```Debug=True``` and the server is run via ```python .../CM-Database/manage.py runserver```.

```Debug=False``` and ```systemctl start httpd``` passes that functionality to the Apache service. This only works when run on HEP11 as it is the only machine configured to work properly with our code (for now).

IMPORTANT:
-
Along with the code in this repo there is also a 21.6 GB 'media' folder that contains... images of the chips, i think? I can't tell what is accessing it.

If you run into issues and need to scp that to your local device, the directory is located on hep01 under the filepath ```/hep01-data1/hep06-copy/django/testing_database_he/media```.

Should be placed next to your github repo folder in a folder named 'QIE_media' for the program to locate it. 

Not including it in the github repo because github did not like it when i tried to push a 86,000 file commit... 
