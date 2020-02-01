from __future__ import unicode_literals
from django.shortcuts import render, Http404
from django.views.generic import TemplateView
from .models import PlantData, Plants
from customuser.models import User
from django.utils.datastructures import MultiValueDictKeyError
from polls import connect
from datetime import datetime
from polls.forms import UserForm, UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
def frontpage(request):
        return render(request, 'frontpage.html')
		#return render(request, 'index.html')
		#return render(request, './logreg/base.html')

def display(request, id):		
		return render(request, 'planttemplate.html', {'id': id, 'obj': connect.getData(id)})

@csrf_exempt
def postdata(request):
    if request.method == "POST":
        try:
            systemId = request.POST.get('SystemId')
            hasBeenRegistered = User.objects.filter(deviceID = request.POST.get('SystemId'))
            measurementTime = datetime.fromtimestamp(int(request.POST.get('MeasurementTime')))
            if hasBeenRegistered:
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
        return render(request, 'myplants.html', {'plants': connect.getPlantData(request.user.deviceID)})
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

@login_required
def special(request):
    return HttpResponse("You are logged in !")
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))##???

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'./logreg/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                ## This is where it fucks up
                return HttpResponseRedirect(('./planttemplate.html'))
                #return(render(request,'planttemplate.html',{'obj':connect.getData()}))
                #return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, './logreg/login.html', {})

class HomeView(TemplateView):
   # template_name = 'index.html'
	template_name = './logreg/index.html'
