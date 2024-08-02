from djongo import models
from django import forms
from djongo.models import CharField, EmbeddedField, ArrayField, DjongoManager

LOCATION_LENGTH = 100
MAX_COMMENT_LENGTH = 1000


class Summary(models.Model):
    passed = CharField(max_length = 3)
    total = CharField(max_length = 3)
    collected = CharField(max_length = 3)

    def __getitem__(self, name):
        return getattr(self, name)
    
    class Meta:
        abstract = True


class Test_Outcome(models.Model):
    test_name = CharField(max_length = 20, null = False)
    #if this works, probably want to replace this with IntegerField or something similar to make sure it can only ever be [-1, 0, 1]
    test_result = CharField(max_length = 1, null = False)
    
    objects = DjongoManager()

    class Meta:
        abstract = True


class Test_Outcome_Form(forms.ModelForm):
    class Meta:
        model = Test_Outcome
        fields = ('test_name','test_result')

'''
class Array_Value(models.Model):
    value = CharField(max_length = 6)

    class Meta:
        abstract = True

class Array_Value_Form(forms.ModelForm): 
    class Meta:
        model = Array_Value
        fields = ('value',)
'''


class eTX_Row(models.Model):
    #_id = models.ObjectIdField()
    eTX1 = CharField(max_length = 6, null = True) 
    eTX2 = CharField(max_length = 6, null = True)
    eTX3 = CharField(max_length = 6, null = True)
    eTX4 = CharField(max_length = 6, null = True)
    eTX5 = CharField(max_length = 6, null = True)
    eTX6 = CharField(max_length = 6, null = True)
    eTX7 = CharField(max_length = 6, null = True)
    eTX8 = CharField(max_length = 6, null = True)
    eTX9 = CharField(max_length = 6, null = True)
    eTX10 = CharField(max_length = 6, null = True)
    eTX11 = CharField(max_length = 6, null = True)
    eTX12 = CharField(max_length = 6, null = True) 
    eTX13 = CharField(max_length = 6, null = True) 
    eTX14 = CharField(max_length = 6, null = True) 
    eTX15 = CharField(max_length = 6, null = True) 
    eTX16 = CharField(max_length = 6, null = True)
    eTX17 = CharField(max_length = 6, null = True)
    eTX18 = CharField(max_length = 6, null = True)
    eTX19 = CharField(max_length = 6, null = True)
    eTX20 = CharField(max_length = 6, null = True)
    eTX21 = CharField(max_length = 6, null = True)
    eTX22 = CharField(max_length = 6, null = True)
    eTX23 = CharField(max_length = 6, null = True)
    eTX24 = CharField(max_length = 6, null = True)
    eTX25 = CharField(max_length = 6, null = True)
    eTX26 = CharField(max_length = 6, null = True)
    eTX27 = CharField(max_length = 6, null = True)
    eTX28 = CharField(max_length = 6, null = True)
    eTX29 = CharField(max_length = 6, null = True)
    eTX30 = CharField(max_length = 6, null = True)
    eTX31 = CharField(max_length = 6, null = True)
    eTX32 = CharField(max_length = 6, null = True)
    eTX33 = CharField(max_length = 6, null = True)
    eTX34 = CharField(max_length = 6, null = True)
    eTX35 = CharField(max_length = 6, null = True)
    eTX36 = CharField(max_length = 6, null = True)
    eTX37 = CharField(max_length = 6, null = True)
    eTX38 = CharField(max_length = 6, null = True)
    eTX39 = CharField(max_length = 6, null = True)
    eTX40 = CharField(max_length = 6, null = True)
    eTX41 = CharField(max_length = 6, null = True)
    eTX42 = CharField(max_length = 6, null = True)
    eTX43 = CharField(max_length = 6, null = True)
    eTX44 = CharField(max_length = 6, null = True)
    eTX45 = CharField(max_length = 6, null = True)
    eTX46 = CharField(max_length = 6, null = True)
    eTX47 = CharField(max_length = 6, null = True)
    eTX48 = CharField(max_length = 6, null = True) 
    eTX49 = CharField(max_length = 6, null = True) 
    eTX50 = CharField(max_length = 6, null = True) 
    eTX51 = CharField(max_length = 6, null = True)
    eTX52 = CharField(max_length = 6, null = True)
    eTX53 = CharField(max_length = 6, null = True)
    eTX54 = CharField(max_length = 6, null = True)
    eTX55 = CharField(max_length = 6, null = True)
    eTX56 = CharField(max_length = 6, null = True)
    eTX57 = CharField(max_length = 6, null = True)
    eTX58 = CharField(max_length = 6, null = True)
    eTX59 = CharField(max_length = 6, null = True)
    eTX60 = CharField(max_length = 6, null = True)
    eTX61 = CharField(max_length = 6, null = True)
    eTX62 = CharField(max_length = 6, null = True)
    eTX63 = CharField(max_length = 6, null = True)
    #eTX64= CharField(max_length = 6, null = True)
    class Meta:
        abstract = True


class eTX_Row_Form(forms.ModelForm):
    class Meta:
        model = eTX_Row
        fields = ('eTX1','eTX2','eTX3','eTX4','eTX5','eTX6','eTX7','eTX8','eTX9','eTX10','eTX11','eTX12')


class eRX_Row(models.Model):
    _id = models.ObjectIdField
    eRX1 = CharField(max_length = 6, null = True) 
    eRX2 = CharField(max_length = 6, null = True)
    eRX3 = CharField(max_length = 6, null = True)
    eRX4 = CharField(max_length = 6, null = True)
    eRX5 = CharField(max_length = 6, null = True)
    eRX6 = CharField(max_length = 6, null = True)
    eRX7 = CharField(max_length = 6, null = True)
    eRX8 = CharField(max_length = 6, null = True)
    eRX9 = CharField(max_length = 6, null = True)
    eRX10 = CharField(max_length = 6, null = True)
    eRX11 = CharField(max_length = 6, null = True)
    eRX12 = CharField(max_length = 6, null = True)

    class Meta:
        abstract = True


class eRX_Row_Form(forms.ModelForm):
    class Meta:
        model = eRX_Row
        fields = ('eRX1','eRX2','eRX3','eRX4','eRX5','eRX6','eRX7','eRX8','eRX9','eRX10','eRX11','eRX12')


class Test_Metadata(models.Model):
    eRX_errcounts = ArrayField(
            model_container = eRX_Row,
            model_form_class = eRX_Row_Form,
            blank = True
            )
    eTX_delays =  ArrayField(
            model_container = eTX_Row,
            model_form_class = eTX_Row_Form,
            blank = True
            )
    eTX_bitcounts =  ArrayField(
            model_container = eTX_Row,
            model_form_class = eTX_Row_Form,
            blank = True
            )
    eTX_errcounts =  ArrayField(
            model_container = eTX_Row,
            model_form_class = eTX_Row_Form,
            blank = True
            )
   
    def __getitem__(self,name):
        return getattr(self,name)

    class Meta:
        abstract = True

class Failure_Info(models.Model):
    #this is currently coded in a very silly way and should be corrected once it becomes clearer what the failure reports will look like
    failure_mode = CharField(max_length = 2000, null = True)
    failure_cause = CharField(max_length = 2000, null = True)
    failure_code_line = CharField(max_length = 2000, null = True)

    class Meta:
        abstract = True

class Test_Details(models.Model):
    test_name = CharField(max_length = 20, null = True)
    test_metadata  = EmbeddedField(model_container = Test_Metadata, null = True)
    #failure_info = EmbeddedField(model_container = Failure_Info, null = True)
    
    objects = DjongoManager()

    class Meta:
        abstract = True

class Test_Details_Form(forms.ModelForm):
    class Meta:
        model = Test_Details
        fields = ('test_name', 'test_metadata')


class Card_Metadata(models.Model):
    branch = CharField(max_length = 20, default = "NO_BRANCH")
    commit_hash = CharField(max_length = 30, default = "NO_COMMIT_HASH")
    remote_url = CharField(max_length = 50, default = "NO_URL")
    status = CharField(max_length = 50, default = "NO_STATUS")
    firmware_name = CharField(max_length = 30, default = "NO_FIRMWARE_NAME")
    firmware_git_desc =  CharField(max_length = 20, default = "NO_GIT_DESC")
    filename = CharField(max_length = 50, default = "NO_FILENAME")

    class Meta:
        abstract = True
   

class CM_Card(models.Model):
    #unsure if manual ID assignment is really necessary but I remember it fixing some issue I had last time I did this
    _id = models.ObjectIdField()
    #identifier is the chip number or barcode or whatnot
    identifier = CharField(max_length = 20, default = "NO_ID_ASSIGNED")
    #Quick Test summary for easy fast data
    summary = EmbeddedField(model_container = Summary, null = True)
    #1 for passed, 0 for failed, -1 for skipped
    test_outcomes = ArrayField(
            model_container = Test_Outcome,
            model_form_class = Test_Outcome_Form,
            null = True)
    test_details = ArrayField(
            model_container = Test_Details,
            model_form_class = Test_Details_Form,
            null = True)
    card_metadata = EmbeddedField(model_container = Card_Metadata, null = True)
    
    objects = DjongoManager()
