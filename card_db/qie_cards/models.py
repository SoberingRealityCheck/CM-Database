from djongo import models
from django import forms
# Create your models here

LOCATION_LENGTH = 100
MAX_COMMENT_LENGTH = 1000
#still need to actually connect these variables to their respective things but that can wait until AFTER the code works at all

'''
class Test_Variable(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    username = models.CharField(max_length=60)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username
'''


class Summary(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    passed = models.CharField(max_length=2, default="")
    total = models.CharField(max_length=2, unique=False, default="")
    collected = models.CharField(max_length=2, unique=False, default="")
    
    def __getitem__(self, name):
        return getattr(self, name)

    class Meta:
        abstract = True

'''
#this Test_Results class just exists for demo purposes and can be safely discarded once it's done
class Test_Results(models.Model):
    created = models.CharField(max_length=20, unique=False, default="")
    duration = models.CharField(max_length=20, unique=False, default="")
    exitcode = models.CharField(max_length=3, unique=False, default="")
    
    summary = models.EmbeddedField(
            model_container = Summary
            )
    
    objects = models.DjongoManager()
'''

#actual test result model structure continues here

class Environment(models.Model):
    environment = models.CharField(max_length=20, null=True, blank=True)
    
    def __getitem__(self, name):
        return getattr(self, name)

    class Meta:
        abstract = True

class Environment_Form(forms.ModelForm):
    _id = models.ObjectIdField(primary_key = True) 
    class Meta:
        model = Environment
        fields = ('environment',)
        abstract = True
        managed = False



class Result(models.Model):
    nodeid = models.CharField(max_length=20, unique=False, default="")
    type = models.CharField(max_length=10, unique=False, default="")
    lineno = models.CharField(max_length=4, unique=False, null=True)
    
    class Meta:
        abstract = True

class Result_Form(forms.ModelForm):
    class Meta:
        model = Result
        fields = ('nodeid','type','lineno')

class Collector(models.Model):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
    nodeid = models.CharField(max_length=20, unique=False, default="", primary_key=True)
    outcome = models.CharField(max_length=20, unique=False, default="")
    result = models.ArrayField(
            model_container = Result,
            model_form_class = Result_Form
            )
    
    objects = models.DjongoManager()

    class Meta:
        managed = False

class Collector_Form(forms.ModelForm):
    class Meta:
        model = Collector
        fields = ('nodeid','outcome','result')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Keyword(models.Model):
    keyword = models.CharField(max_length=50, unique=False, default="")
    print(keyword)
    class Meta: 
        abstract = True

class Keyword_Form(forms.ModelForm):
    class Meta:
        model = Keyword
        fields = ('keyword',)

class Setup(models.Model): 
    duration = models.CharField(max_length=20, default="")
    outcome = models.CharField(max_length=10, unique=False, default="")
    stdout = models.CharField(max_length=200, unique=False, null=True)
    def __getitem__(self, name):
        return getattr(self, name)

    class Meta:
        abstract = True
'''
class eRX_Errcounts(models.Model):
    eRX_Errcount = models.CharField(max_length = 50, default="")
    
    class Meta:
        abstract = True

class eRX_Errcounts_Form(forms.ModelForm):
    class Meta:
        model = eRX_Errcounts
        fields = ('eRX_Errcount',)
'''


class Metadata(models.Model):
    _id = models.ObjectIdField()
    '''
    eRX_errcounts = models.ArrayField(
            model_container = eRX_Errcounts,
            model_form_class = eRX_Errcounts_Form
            )
    '''
    eTX_delays = models.CharField(max_length=500, unique=False, null=True)
    eTX_bitcounts = models.CharField(max_length=500, unique=False, null=True)
    eTX_errcounts = models.CharField(max_length=500, unique=False, null=True)
    eRX_errcounts = models.CharField(max_length=500, unique=False, null=True)
    maxwidth = models.CharField(max_length = 50, unique=False, null=True)
    second_max_width = models.CharField(max_length=50, unique=False, null=True)    
    

    def __getitem__(self, name):
        return getattr(self, name)

    class Meta:
        abstract = True
    
   

class Metadata_Form(forms.ModelForm):
    class Meta:
        model = Metadata
        fields = ('eTX_delays','eTX_bitcounts','eTX_errcounts','eRX_errcounts','maxwidth','second_max_width')

'''
class Log(models.Model):
    _id = models.ObjectIdField()
    
    name = models.CharField(max_length=20, unique=False, default="")
    msg = models.CharField(max_length=50, unique=False, default="")
    args = models.CharField(max_length=50, unique=False, default="")
    levelname = models.CharField(max_length=50, unique=False, default="")
    levelno = models.CharField(max_length=3, unique=False, default="")
    pathname = models.CharField(max_length=50, unique=False, default="")
    filename = models.CharField(max_length=30, unique=False, default="")
    module = models.CharField(max_length=30, unique=False, default="")
    exc_info = models.CharField(max_length=30, unique=False, default="")
    exc_text = models.CharField(max_length=400, unique=False, default="")
    stack_info = models.CharField(max_length=50, unique=False, default="")
    lineno = models.CharField(max_length=4, unique=False, default="")
    funcName = models.CharField(max_length=20, unique=False, default="")
    created = models.CharField(max_length=40, unique=False, default="")
    msecs = models.CharField(max_length=40, unique=False, default="")
    relativeCreated = models.CharField(max_length=40, unique=False, default="")
    thread = models.CharField(max_length=40, unique=False, default="")
    threadName = models.CharField(max_length=20, unique=False, default="")
    processName = models.CharField(max_length=20, unique=False, default="")
    process = models.CharField(max_length=7, unique=False, default="")
     
    def __getitem__(self, name):
        return getattr(self, name)
    
    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        abstract=True

class Log_Form(forms.ModelForm):
    class Meta:
        model = Log
        fields = ('name','msg','args','levelname','levelno','pathname','filename',
                'module','exc_info','exc_text','stack_info','lineno','funcName','created',
                'msecs','relativeCreated','thread','threadName','processName','process')
'''
class Call(models.Model):
    _id = models.ObjectIdField()
    duration = models.CharField(max_length=20, default="")
    outcome = models.CharField(max_length=10, unique=False, default="")   
    
    log = models.CharField(max_length=2000, unique=False, null = True)
    
    
    objects = models.DjongoManager()
    def __str__(self):
        return f'{self.duration}'
    '''
    def __getitem__(self, name):
        return getattr(self, name)
    '''
    class Meta:
        abstract = True

class Teardown(models.Model):
    duration = models.CharField(max_length=20, default="")
    outcome = models.CharField(max_length=10, unique=False, default="")   

    def __getitem__(self, name):
        return getattr(self, name)

    class Meta:
        abstract = True


class Test(models.Model):
    nodeid = models.CharField(max_length=20, unique=False, default="")
    lineno = models.CharField(max_length=4, unique=False, default="")
    outcome = models.CharField(max_length=10, unique=False, default="")
    keywords = models.ArrayField(
            model_container = Keyword,
            model_form_class = Keyword_Form
            )
    metadata = models.EmbeddedField(
            model_container = Metadata,
            #model_form_class = Metadata_Form,
            null = True
            )
    setup = models.EmbeddedField(model_container=Setup)
    call = models.EmbeddedField(model_container=Call)
    teardown = models.EmbeddedField(model_container=Teardown)
    
    objects = models.DjongoManager()

    class Meta:
        abstract = True

class Test_Form(forms.ModelForm):
    class Meta:
        model = Test
        fields = ('nodeid','lineno','outcome','keywords',
                'setup','metadata','call','teardown'
                )

class CM_Test_Results(models.Model):
    _id = models.ObjectIdField()
    created = models.CharField(max_length=20, default="")
    duration = models.CharField(max_length=20, unique=False, default="")
    exitcode = models.CharField(max_length=3, unique=False, default="")
    root = models.CharField(max_length=50, unique=False, default="")
    '''
    environment = models.ArrayField(
            model_container = Environment,
            )
    '''
    environment = models.EmbeddedField(model_container = Environment)

    summary = models.EmbeddedField(model_container = Summary)
    
    
    collectors = models.ArrayField(
            model_container = Collector,
            model_form_class = Collector_Form
            )
    
    tests = models.ArrayField(
            model_container = Test,
            model_form_class = Test_Form
            )
    

    
    FPGA_hexa_IP = models.CharField(max_length=5, unique=False, default="")
    branch = models.CharField(max_length=20, unique=False, default="")
    commit_hash = models.CharField(max_length=50, unique=False, default="")
    remote_url = models.CharField(max_length=50, unique=False, default="")
    status = models.CharField(max_length=200, unique=False, default="")
    firmware_name = models.CharField(max_length=50, unique=False, default="")
    chip_number = models.CharField(max_length=50, unique=False, default="null")
    
    objects = models.DjongoManager()
    
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    '''
    

    
