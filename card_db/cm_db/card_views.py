import sqlite3
from django.shortcuts import render
from django.views import generic
import datetime
from os import listdir, path
import json

#from .models import CM_Card, Tester, Test, Attempt, Location, CMShuntParams 
import cm_db.custom.filters as filters
from .models import CM_Card
# Create your views here.

from django.utils import timezone
from django.http import HttpResponse, Http404
from card_db.settings import MEDIA_ROOT, CACHE_DATA 


class CatalogView(generic.ListView):
    """ This displays a list of all CM cards """
    
    template_name = 'cm_db/catalog.html'
    context_object_name = 'filename_url_list'
    cards = CM_Card.objects.all().order_by('filename_url')
    #num_cards = len(cards)
    def get_queryset(self):
        return self.cards
    def numberCards(self):
        return len(self.cards)

def catalog(request):
    """ This displays a list of all CM cards """
    cards = CM_Card.objects.all().order_by('filename_url')
    count = len(cards)

    return render(request, 'cm_db/catalog.html', {'filename_url_list': cards,
                                                      'total_count': count})

def summary(request):
    """ This displays a summary of the cards """
    if CACHE_DATA:
        cache = path.join(MEDIA_ROOT, "cached_data/summary.json")
        print("opening JSON")
        infile = open(cache, "r")
        print("opened JSON")
        print("Loading JSON")
        cardStat = json.load(infile)
        print("JSON Loaded")
    else:
        print("Loading Cards")
        cards = list(CM_Card.objects.all().order_by('identifier'))
        print("Loaded Cards")
        print("Loading Tests")
        tests = list(Test.objects.all())
        print("Loaded Tests")
        print("Loading Attempts")
        attempts = list(Attempt.objects.all())
        print("Loaded Attempts")
        print("Getting States!")
        cardStat = filters.getCardTestStates(cards, tests, attempts)
        print("Got 'em!")
    
    return render(request, 'cm_db/summary.html', {'cards': cardStat})


def calibration(request, card):
    """ This displays the calibration overview for a card """
    if len(card) > 7:
        try:
            p = CM_Card.objects.get(uid__endswith=card)
        except CM_Card.DoesNotExist:
            raise Http404("CM card with unique id " + str(card) + " does not exist")
    else:
        try:
            p = CM_Card.objects.get(identifier__endswith=card)
        except CM_Card.DoesNotExist:
            raise Http404("CM card with identifier " + str(card) + " does not exist")

    calibrations = p.CMshuntparams_set.all().order_by("group")

    return render(request, 'cm_db/calibration.html', {'card': p, 'cals': list(calibrations)})

def calResults(request, card, group):
    """ This displays the calibration results for a card """
    if len(card) > 7:
        try:
            p = CM_Card.objects.get(uid__endswith=card)
        except CM_Card.DoesNotExist:
            raise Http404("CM card with unique id " + str(card) + " does not exist")
    else:
        try:
            p = CM_Card.objects.get(identifier__endswith=card)
        except CM_Card.DoesNotExist:
            raise Http404("CM card with identifier " + str(card) + " does not exist")
    calibration = p.CMshuntparams_set.get(group=group)

    if str(calibration.results) != "default.png":
        conn = sqlite3.connect(path.join(MEDIA_ROOT, str(calibration.results)))
        c = conn.cursor()
        c.execute("select * from CMshuntparams")
        data = []
        for item in c:
            temp = { "id":str(item[0]),
                     "serial":str(p.identifier),
                     "CM":str(item[2]),
                     "capID":str(item[3]),
                     "range":str(item[4]),
                     "shunt":str(item[5]),
                     "date":str(item[7]),
                     "slope":str(item[8]),
                     "offset":str(item[9]),
                    }
            data.append(temp)
    return render(request, 'cm_db/cal_results.html', {'card': p,
                                                          'data': data,
                                                         })

def calPlots(request, card, group):
    """ This displays the calibration plots for a card """
    if len(card) > 7:
        try:
            p = CM_Card.objects.get(uid__endswith=card)
        except CM_Card.DoesNotExist:
            raise Http404("CM card with unique id " + str(card) + " does not exist")
    else:
        try:
            p = CM_Card.objects.get(identifier__endswith=card)
        except CM_Card.DoesNotExist:
            raise Http404("CM card with identifier " + str(card) + " does not exist")
    calibration = p.CMshuntparams_set.get(group=group)

    files = []

    if str(calibration.plots) != "default.png" and path.isdir(path.join(MEDIA_ROOT, str(calibration.plots))):
        for f in listdir(path.join(MEDIA_ROOT, str(calibration.plots))):
            files.append(path.join(calibration.plots.url, path.basename(f)))
    else:
        files.append("No Data!")
    return render(request, 'cm_db/cal_plots.html', {'card': p,
                                                        'plots': files,
                                                         })
class TestersView(generic.ListView):
    """ This displays the users and email addresses """
    
    template_name = 'cm_db/testers.html'
    context_object_name = 'tester_list'
    def get_queryset(self):
        return Tester.objects.all().order_by('username')


class TestDetailsView(generic.ListView):
    """ This displays the tests and their descriptions """

    template_name = 'cm_db/test-details.html'
    context_object_name = 'test_list'
    def get_queryset(self):
        return Test.objects.all().order_by('name')


def stats(request):
    """ This displays a summary of the cards """
   
    # Get required attempts and tests
    if CACHE_DATA:
        cache = path.join(MEDIA_ROOT, "cached_data/stats.json")
        infile = open(cache, "r")
        statistics = json.load(infile)
    else:
        attempts = []
        tests = list(Test.objects.filter(required=True))
        
        for test in tests:
            attempts.extend(list(test.attempt_set.all())) 
                
        cards = list(CM_Card.objects.all().order_by("identifier"))

        testFailedStats = filters.getFailedCardStats(cards, tests, attempts)
        testPassedStats = filters.getPassedCardStats(cards, tests, attempts)
        testRemStats = filters.getRemCardStates(cards, tests, attempts)
        statistics = {'passed': testPassedStats,
                      'failed': testFailedStats,
                      'remaining': testRemStats,
                     }

    return render(request, 'cm_db/stats.html', statistics)

def detail(request, card):
    print(card)
    """ This displays the overview of tests for a card """
    if len(card) > 7:
        try:
            p_results = CM_Card.objects.filter(filename_url = card)
        except CM_Card.DoesNotExist:
            #raise Http404("CM card with unique id " + str(card) + " does not exist")
            return render(request, 'cm_db/error.html')
    else:
        try:
            #p_results = CM_Card.objects.get(identifier__endswith=card)
            p_results = CM_Card.objects.all().filter(identifier = card)
            print("p results:",p_results) 
        except CM_Card.DoesNotExist:
            #raise Http404("CM card with identifier " + str(card) + " does not exist")
            return render(request, 'cm_db/error.html')
    for p in p_results:
        print("chip number:", p.identifier)
        '''
        locations = Location.objects.filter(card=p)
        '''
        attempts = []
        status = {}    
        tests = p.test_outcomes

        status["total"] = p.summary["total"]
        status["passed"] = p.summary["passed"]
        status["collected"] = p.summary["collected"]
        status["error"] = p.summary["error"]
        failedAny = False
        forcedAny = False

        for test in tests:
            name = test["test_name"]
            result = test["test_result"]
            if result == 1:
                attempts.append({"attempt":name, "valid":True})
            if result == 0:
                attempts.append({"attempt":name, "valid":False})
                failedAny = True
            if result == -1:
                attempts.append({"attempt":name, "valid":True})
                forcedAny = True
            ''' 
            attemptList = attempts[nodeid==test].order_by("attempt_number")
            if attemptList:
                last = attemptList[len(attemptList)-1]
                if not last.revoked and test.required:
                    if last.overwrite_pass:
                        status["passed"] += 1
                        forcedAny = True
                    elif last.passed_all():
                        status["passed"] += 1
                    else:
                        failedAny = True
                attempts.append({"attempt":last, "valid": True, "required": test.required})
            else:
                attempts.append({"attempt":test.test_name, "valid": False, "required": test.required})
            '''

        if status["total"] == status["passed"]:
            if forcedAny:
                status["banner"] = "GOOD (FORCED)"
                status["css"] = "forced"
            else:
                status["banner"] = "GOOD"
                status["css"] = "okay"
        elif failedAny:
            status["banner"] = "FAILED"
            status["css"] = "bad"
        else:
            status["banner"] = "INCOMPLETE"
            status["css"] = "warn"

        if(request.POST.get('comment_add')):
            comment = ""
            if not p.comments == "":
                comment += "\n"
            comment += str(timezone.now().date()) + " " + str(timezone.now().hour) + "." + str(timezone.now().minute) + ": " + request.POST.get('comment')
            tempcomments = p.comments
            if not tempcomments:
                tempcomments = ""
            tempcomments += comment
            p.comments = tempcomments
            p.save()

        if(request.POST.get('location_add')):      
            newloc = {"geo_loc":request.POST.get("location")}
            newloc["date_received"] = str(timezone.now().date()) + " " + str(timezone.now().hour) + "." + str(timezone.now().minute)
            temploc = p.locations
            if not temploc:
                temploc = []
            temploc.append(newloc)
            p.locations = temploc
            p.save()
        return render(request, 'cm_db/detail.html', {'card': p,
                                                         'rm' : "PLACEHOLDER",
                                                         'rm_slot' : "PLACEHOLDER",
                                                         'cu' : "PLACEHOLDER",
                                                         'attempts':attempts,
                                                         'locations':"PLACEHOLDER",
                                                         'status':status,
                                                        })

#class CatalogView(generic.ListView):
#    """ This displays a list of all CM cards """
#    
#    template_name = 'cm_db/catalog.html'
#    context_object_name = 'identifier_list'
#    def get_queryset(self):
#        return CM_Card.objects.all().order_by('identifier')
#
def error(request): 
    """ This displays an error for incorrect identifier or unique id """
    return render(request, 'cm_db/error.html')

class PlotView(generic.ListView):
    """ This displays various plots of data """
    
    template_name = 'cm_db/plots.html'
    context_object_name= 'tests'
    def get_queryset(self):
        return list(Test.objects.all())

def testDetail(request, card, test):
    """ This displays details about a specific test for a card """
    if len(card) > 7:
        try:
            p = CM_Card.objects.get(uid__endswith=card)
        except CM_Card.DoesNotExist:
            raise Http404("CM card with unique id " + str(card) + " does not exist")
    else:
        try:
            p = CM_Card.objects.get(identifier__endswith=card)
        except CM_Card.DoesNotExist:
            raise Http404("CM card with identifier " + str(card) + " does not exist")
    try:
        curTest = Test.objects.get(name=test)
    except CM_Card.DoesNotExist:
        raise Http404("CM card does not exist")
    
    if(request.POST.get('overwrite_pass')):
        if(request.POST.get('secret') == "pseudo" or request.POST.get('secret') == "pseudopod"):
            attempt = Attempt.objects.get(pk=request.POST.get('overwrite_pass'))
            attempt.overwrite_pass = not attempt.overwrite_pass
            attempt.save()
    
    attemptList = list(Attempt.objects.filter(card=p, test_type=curTest).order_by("attempt_number").reverse())
    attemptData = []
    for attempt in attemptList:
        data = ""
        if not str(attempt.hidden_log_file) == "default.png":
            inFile = open(path.join(MEDIA_ROOT, str(attempt.hidden_log_file)), "r")
            tempDict = json.load(inFile)
            if attempt.test_type.abbreviation == "overall pedestal" and "pedResults" in tempDict["TestOutputs"]: 
                data = tempDict["TestOutputs"]["pedResults"]
            elif attempt.test_type.abbreviation == "overall charge injection" and "ciResults" in tempDict["TestOutputs"]: 
                data = tempDict["TestOutputs"]["ciResults"]
            elif attempt.test_type.abbreviation == "overall phase scan" and "phaseResults" in tempDict["TestOutputs"]:
                data = tempDict["TestOutputs"]["phaseResults"]
            elif attempt.test_type.abbreviation == "overall shunt scan" and "shuntResults" in tempDict["TestOutputs"]:
                data = tempDict["TestOutputs"]["shuntResults"]
            elif "ResultStrings" in tempDict:
                if attempt.test_type.abbreviation in tempDict["ResultStrings"]:
                    data = tempDict["ResultStrings"][attempt.test_type.abbreviation]
        attemptData.append((attempt, data))

    firstTest = []

    return render(request, 'cm_db/testDetail.html', {'card': p,
                                                         'test': curTest,
                                                         'attempts': attemptData
                                                         })


def fieldView(request):
    """ This displays details about tests on a card """ 
    options = ["identifier",
               "readout_module",
               "calibration_unit",
               "uid",
               "bridge_major_ver",
               "bridge_minor_ver",
               "bridge_other_ver",
               "igloo_major_ver",
               "igloo_minor_ver",
               "comments",
               "last location",
               "Card Status"]
    
    fields = []
    for i in range(5):
        if(request.POST.get('field' + str(i+1))):
            field = request.POST.get('field' + str(i+1))
            if field in options:
                fields.append(field)


    cards = list(CM_Card.objects.all().order_by("identifier"))
    items = []
    # Info for "Card Status"
    cache = path.join(MEDIA_ROOT, "cached_data/summary.json")
    infile = open(cache, "r")
    cardStat = json.load(infile)
    num_required = len(Test.objects.filter(required=True))
    infile.close()
    
    for i in range(len(cards)):
        card = cards[i]
        item = {}
        item["id"] = card.pk
        item["fields"] = []
        for field in fields:
            if field == "last location":
                loc_list = card.location_set.all()
                if len(loc_list) == 0:
                    item["fields"].append("No Locations Recorded")
                else:
                    #item["fields"].append(len(card.location_set.all()))
                    item["fields"].append(card.location_set.all().order_by("date_received").reverse()[0].geo_loc)
            elif field == "Card Status":
                if cardStat[i]["num_failed"] != 0:
                    item["fields"].append("FAILED")
                elif cardStat[i]["num_passed"] == num_required:
                    if cardStat[i]["forced"]:
                        item["fields"].append("GOOD (FORCED)")
                    else:
                        item["fields"].append("GOOD")
                else:
                    item["fields"].append("INCOMPLETE")
            else:
                item["fields"].append(getattr(card, field))

        items.append(item)

    return render(request, 'cm_db/fieldView.html', {'fields': fields, "items": items, "options": options})

