# Create your views here.
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Location
import requests
from datetime import date, timedelta, datetime



def index(request):
    template = loader.get_template('polls/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def getData(request):
    today = date.today()
    # dd/mm/YY
    d1 = today
    daysSub = timedelta(1)
    d1 = d1 - daysSub
    target=get_object_or_404(Location, name="Hong Kong")

    covidData={}
    error_message=""
    if (target!=None):
        if (d1!=""):
            dList=[(d1-timedelta(i+1)).strftime("%d/%m/%Y") for i in range(7)]
            print(dList)
            d1 = (d1.strftime("%d/%m/%Y"))
            response = requests.get(target.apiString)
            dictList=[]
            avgNewCases=0
            avgNewDeaths=0
            na= False
            for dict in response.json():
                #print(d1)
                #print(dict['As of date'])
                if dict['As of date'] == d1:
                    covidData=dict
                    #print("found")
                elif dict['As of date'] in dList:
                    if (not na and (dict["Number of cases fulfilling the reporting criteria"]!="" or dict["Number of cases fulfilling the reporting criteria"]!="")):
                        avgNewCases=avgNewCases+int(dict["Number of cases fulfilling the reporting criteria"])
                        avgNewDeaths=avgNewDeaths+int(dict["Number of cases fulfilling the reporting criteria"])
                    else:
                        avgNewCases=0
                        avgNewDeaths=0
                        na=True
                    #print(dict)
            #covidData=response.json()[0]['As of date']
            if covidData!={}:
                covidData["As of date"]=datetime.strptime(covidData["As of date"], "%d/%m/%Y").strftime("%Y-%m-%d")
                covidData["confirmedCasesMillion"]=int(covidData["Number of confirmed cases"])/1000000
                covidData["deathCasesMillion"]=int(covidData["Number of death cases"])/1000000
                covidData["avgNewCases"]=avgNewCases/7
                covidData["avgNewDeaths"]=avgNewDeaths/7
                #print("Cases per million", covidData["confirmedCasesMillion"])
            else:
                error_message="Data not found"
        else:
            error_message="Please enter correct date"
    else:
        error_message="Please choose a location first"
    template = loader.get_template('polls/retrieveResults.html')
    context = {"target":target, "covidData":covidData, "Location":Location.objects.all(), "error_message":error_message}
    return HttpResponse(template.render(context, request))


def searchData(request):
    covidData={}
    target={}
    error_message=""
    if (request.POST["locationName"]!="None"):
        if (request.POST["dateAsOf"]!=""):
            d1 = request.POST["dateAsOf"]
            d1 = (datetime.strptime(d1,"%Y-%m-%d"))
            d1 = d1.strftime("%d/%m/%Y")
            d1 = datetime.strptime(d1, "%d/%m/%Y")
            target=get_object_or_404(Location, name=request.POST["locationName"])
            dList=[(d1-timedelta(i)).strftime("%d/%m/%Y") for i in range(8)]
            #print(dList)
            d1 = (d1.strftime("%d/%m/%Y"))
            response = requests.get(target.apiString)
            dictList=[]
            avgNewCases=0
            avgNewDeaths=0
            na= False
            prevNewCases=0
            prevDeathCases=0
            firstTime=True
            for dict in response.json():
                if dict['As of date'] == d1:
                    covidData=dict
                if dict['As of date'] in dList:
                        if dict['As of date'] == d1:
                            covidData=dict
                            covidData["newConfirmedCases"]=int(dict["Number of confirmed cases"])-prevNewCases
                            #print("cases: ", prevNewCases)
                            covidData["newDeathCases"]=int(dict["Number of death cases"])-prevDeathCases
                        if firstTime:
                            prevNewCases=int(dict["Number of confirmed cases"])
                            prevDeathCases=int(dict["Number of death cases"])
                            firstTime=False
                        else:
                            avgNewCases=avgNewCases-prevNewCases+int(dict["Number of confirmed cases"])
                            avgNewDeaths=avgNewDeaths-prevDeathCases+int(dict["Number of death cases"])
                            prevNewCases=int(dict["Number of confirmed cases"])
                            prevDeathCases=int(dict["Number of death cases"])
                            #print(avgNewCases)
            if covidData!={}:
                covidData["As of date"]=datetime.strptime(covidData["As of date"], "%d/%m/%Y").strftime("%Y-%m-%d")
                covidData["confirmedCasesMillion"]=int(covidData["Number of confirmed cases"])/1000000
                covidData["deathCasesMillion"]=int(covidData["Number of death cases"])/1000000
                covidData["avgNewCases"]=avgNewCases/7
                covidData["avgNewDeaths"]=avgNewDeaths/7
                #print("Cases per million", covidData["confirmedCasesMillion"])
            else:
                error_message="Data not found"
        else:
            error_message="Please enter correct date"
    else:
        error_message="Please choose a location first"
    template = loader.get_template('polls/retrieveResults.html')
    context = {"target":target, "covidData":covidData, "Location":Location.objects.all(), "error_message":error_message}
    return HttpResponse(template.render(context, request))



def addData(request):
    template = loader.get_template('polls/saveLocation.html')
    context = {}
    return HttpResponse(template.render(context, request))

def saveLocation(request):
    location=Location()
    location.name=request.POST["locationName"]
    location.population=request.POST["population"]
    location.apiString=request.POST["apiString"]
    location.urlString=request.POST["urlString"]
    location.save()
    template = loader.get_template('polls/results.html')
    context = {'location': location}
    return HttpResponse(template.render(context, request))
