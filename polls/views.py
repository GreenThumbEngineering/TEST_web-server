from __future__ import unicode_literals
from django.shortcuts import render, Http404
from django.views.generic import TemplateView
from .models import PlantData, Plants, NDVIMeasurement, Water
from customuser.models import User
from django.utils.datastructures import MultiValueDictKeyError
from datetime import datetime, timedelta
from polls.forms import UserForm, UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import PlantsForm
from django.shortcuts import redirect
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .forms import NDVIForm, WaterForm
from ai import prediction as prediction

class PlantUpdate(UpdateView):
    model = Plants
    fields = ['nickname', 'plant_pic']
    template_name_suffix = '_update_form'
    success_url = "/myplants/{id}"

    def dispatch(self, request, *args, **kwargs):
        if not (self.request.user == self.get_object().user):
            raise Http404
        return super(UpdateView, self).dispatch(request, *args, **kwargs)

def frontpage(request):
    if request.user.is_authenticated:
        return myplants(request)
    else: 
        return render(request, 'frontpage.html')

def display(request, id):


    time_threshold = datetime.now() - timedelta(hours=24)
    time_threshold2 = datetime.now() - timedelta(days=7)
    plantinfo = Plants.objects.filter(user=request.user).get(id=id)
    waters = Water.objects.filter(Plant=plantinfo)


    waterdates = []

    for plant in waters:
        waterdates.append(str(plant.MeasurementTime))

    datas = PlantData.objects.filter(DeviceId=plantinfo.deviceid).order_by('-ServerTime') #.filter(ServerTime__gt=time_threshold)
    ndvidata = NDVIMeasurement.objects.filter(Plant=plantinfo) #.filter(MeasurementTime__gt=time_threshold2)

    dates = []
    ndvidates = []

    for plant in datas:
        dates.append(str(plant.ServerTime))
    
    for plant in ndvidata:
        ndvidates.append(str(plant.MeasurementTime))

    if request.method == 'POST':
        if request.POST.get('NDVI_value'):
            ndviform = NDVIForm(request.POST)

            if ndviform.is_valid():
                ndviform.instance.Plant = plantinfo
                ndviform.save()
                waterform = WaterForm()
        else: 
            waterform = WaterForm(request.POST)
            
            if waterform.is_valid():
                waterform.instance.Plant = plantinfo
                waterform.save()
                ndviform = NDVIForm()
    else:    
        ndviform = NDVIForm()
        waterform = WaterForm()

    return render(request, 'planttemplate.html', {'plantinfo': plantinfo, 'id': id, 'plantdatas': datas, 'ndviform': ndviform, 'waterform': waterform, 'dates': dates, 'ndvidates': ndvidates, 'ndvidata': ndvidata, 'waters': waters, 'waterdates': waterdates})

@csrf_exempt
def postdata(request):
    if request.method == "POST":
        try:
            systemId = request.POST.get('SystemId')
            hasBeenRegistered = User.objects.filter(deviceID = request.POST.get('SystemId'))
            measurementTime = datetime.fromtimestamp(int(request.POST.get('MeasurementTime')))
            
            if hasBeenRegistered.count() > 0:               
                for users in hasBeenRegistered:
                    plants = Plants.objects.filter(user_id = users.id)
                    
                    deviceids = []

                    for plant in plants:
                        deviceids.append(plant.deviceid)

                    
                    if request.POST.get('DeviceId') not in deviceids:
                        plant = Plants()
                        plant.user_id = users.id
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
        plants = Plants.objects.filter(user=request.user.id).order_by('nickname')
        time_threshold = datetime.now() - timedelta(hours=4)
        plantswithdata = []

        for plant in plants:
            if PlantData.objects.filter(DeviceId=plant.deviceid).exists():
                plantswithdata.append([plant, PlantData.objects.filter(DeviceId=plant.deviceid).latest('ServerTime').ServerTime.replace(tzinfo=None) > time_threshold.replace(tzinfo=None), PlantData.objects.filter(DeviceId=plant.deviceid).latest('ServerTime')])
            else: 
                plantswithdata.append([plant, bool(False), PlantData.objects.filter(DeviceId=plant.deviceid).latest('ServerTime')])
        return render(request, 'myplants.html', {'plants': plantswithdata})
    else:
        return redirect('/')

def addplant(request):
    if request.user.is_authenticated:
        if request.method == 'POST':           
            form = PlantsForm(request.POST, request.FILES)
            if form.is_valid():
                form.instance.user = request.user

                form.save()
                return myplants(request)
        else:
            form = PlantsForm()
        
        return render(request, 'addplant.html', {'form': form})
