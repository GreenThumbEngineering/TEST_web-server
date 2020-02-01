from __future__ import unicode_literals
from django.shortcuts import render, Http404
from django.views.generic import TemplateView
from .models import PlantData, Plants
from customuser.models import User
from django.utils.datastructures import MultiValueDictKeyError
from datetime import datetime
from polls.forms import UserForm, UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

def frontpage(request):
        return render(request, 'frontpage.html')

def display(request, id):		
		return render(request, 'planttemplate.html', {'id': id, 'plantdatas': PlantData.objects.filter(DeviceId=id)})

@csrf_exempt
def postdata(request):
    if request.method == "POST":
        try:
            systemId = request.POST.get('SystemId')
            hasBeenRegistered = User.objects.filter(deviceID = request.POST.get('SystemId'))
            measurementTime = datetime.fromtimestamp(int(request.POST.get('MeasurementTime')))
            
            if hasBeenRegistered:               
                for users in hasBeenRegistered:
                    plants = Plants.objects.filter(userid = users.id)
                    
                    if request.POST.get('DeviceId') not in list(plants.values('deviceid')):
                        plant = Plants()
                        plant.userid = users.id
                        plant.nickname = request.POST.get('DeviceId')
                        plant.deviceid = request.POST.get('DeviceId')
                        plant.save()

                plantData = PlantData.objects.create(DeviceId = request.POST.get('DeviceId'), SystemId = request.POST.get('SystemId'), MeasurementTime = measurementTime,   Temperature = float(request.POST.get('Temperature')), Humidity = float(request.POST.get('Humidity')) , SoilMoisture = int(request.POST.get('SoilMoisture')), Luminosity = int(request.POST.get('Luminosity')))
                plantData.save()
                return HttpResponse('')
            else:
                raise Http404
            
        except Exception as e:
            print(e)
            raise Http404
    else:
        raise Http404

def myplants(request):
    if request.user.is_authenticated:
        return render(request, 'myplants.html', {'plants': Plants.objects.filter(userid=request.user.id)})
    else:
        return HttpResponse("You are not logged in !")

def addplant(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST.get('nickname') and request.POST.get('deviceid'):
                plant = Plants()
                plant.userid = request.user.id
                plant.nickname = request.POST.get('nickname')
                plant.deviceid = request.POST.get('deviceid')
                plant.save()

                return render(request, 'addplant.html')
        else:
            return render(request, 'addplant.html')
    else:
        return HttpResponse("You are not logged in !")

####
def index(request):
    return render(request,'./logreg/index.html')

class HomeView(TemplateView):
   # template_name = 'index.html'
	template_name = './logreg/index.html'
