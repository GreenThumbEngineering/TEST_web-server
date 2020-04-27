from __future__ import unicode_literals
from django.shortcuts import render, Http404
from django.views.generic import TemplateView
from .models import PlantData, Plants, Water
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
from .forms import WaterForm
from ai import prediction as prediction
from polls import imageprocess as process
from polls import omiparsers
from polls import vpd as VPD
from django.conf import settings
from polls.models import PlantData
import xml.etree.ElementTree as ET
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
from math import exp
from django.utils import timezone
from read_wrapper import ReadWrapper

class PlantUpdate(UpdateView):
    model = Plants
    fields = ['nickname', 'plant_pic']
    template_name_suffix = '_update_form'
    success_url = "/myplants/{id}"

    def dispatch(self, request, *args, **kwargs):
        if not (self.request.user == self.get_object().user):
            raise Http404
        return super(UpdateView, self).dispatch(request, *args, **kwargs)

class PlantDataUpdate(UpdateView):
    model = PlantData
    template_name_suffix = '_update_form'
    fields = ['NDVI_grade']
    success_url = "/grade"
    
    def get_object(self, queryset=None):
        try:
            if self.request.GET.get("return") and "plantdataid" in self.request.session:
                return PlantData.objects.get(id=self.request.session["plantdataid"])
            else: 
                return PlantData.objects.filter(NDVI_grade__isnull=True).order_by('ServerTime')[0]
        except (PlantData.DoesNotExist, IndexError):
            raise Http404

    def dispatch(self, request, *args, **kwargs): 

        if not (self.request.user.is_authenticated):
            raise Http404

        if not self.get_object():
            return redirect('/')

        return super().dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        self.object = form.save()
        self.request.session["plantdataid"] = self.object.id
        return HttpResponseRedirect(self.get_success_url()) 
    

def frontpage(request):
    if request.user.is_authenticated:
        return myplants(request)
    else: 
        return render(request, 'frontpage.html')


def display(request, id):
    plantinfo = Plants.objects.filter(user=request.user).get(id=id)
    
    waters = Water.objects.filter(Plant=plantinfo)
    waterdates = []

    for plant in waters:
        waterdates.append(str(plant.MeasurementTime))

    datas = PlantData.objects.filter(DeviceId=plantinfo.deviceid).order_by('-ServerTime')

    datarow = datas[0]

    problem, status, explanation, instructions = VPD.VPD.vpdAnalysis(datarow.Humidity, datarow.Temperature)
    
    ndviproblem, ndvistatus, ndviexplanation, ndviinstructions = VPD.VPD.ndviAnalysis(datarow.NDVI_value)

    vpdAnalysis = status + explanation + instructions
    ndviAnalysis = ndvistatus + ndviexplanation + ndviinstructions

    dates = []

    for plant in datas:
        dates.append(str(plant.ServerTime))

    if request.method == 'POST':
        waterform = WaterForm(request.POST)
            
        if waterform.is_valid():
            waterform.instance.Plant = plantinfo
            waterform.save()
    else:
        waterform = WaterForm()

    return render(request, 'planttemplate.html', {'plantinfo': plantinfo, 'id': id, 'plantdatas': datas, 'waterform': waterform, 'dates': dates, 'waters': waters, 'waterdates': waterdates, 'vpdAnalysis': vpdAnalysis, 'ndviAnalysis': ndviAnalysis})


@csrf_exempt
def odfread(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            plants = Plants.objects.filter(user=request.user.id).order_by('nickname')
            stringgi = request.POST.get("var1")
            stringgi2= stringgi.replace('&lt;','<')
            stringgi3 = stringgi2.replace('&gt;','>')
            ESP_list = []
            for plant in plants:
                ESP_list.append(plant.deviceid)
            rasp_id = PlantData.objects.values('SystemId')
            RASP = (rasp_id[0]['SystemId'])
            try:
                omi_read_response = ReadWrapper.main(stringgi3)
                response_message = f'''{omi_read_response}'''
                return render(request, 'odfread.html', {'esplist': ESP_list, 'raspid': RASP, 'response_message': response_message})
            except:
                return redirect('/odfread')
        else:
            plants = Plants.objects.filter(user=request.user.id).order_by('nickname')
            ESP_list = []
            for plant in plants:
                ESP_list.append(plant.deviceid)
            rasp_id = PlantData.objects.values('SystemId')
            RASP = (rasp_id[0]['SystemId'])
            return render(request, 'odfread.html', {'esplist': ESP_list, 'raspid':RASP } )


@csrf_exempt
def postdata(request):
    if request.method == "POST":
        try:

            datarequest, rasp_id = omiparsers.WriteParser.main(request.POST['omi_message'])

            hasBeenRegistered = User.objects.filter(deviceID = rasp_id)
            
            if hasBeenRegistered.exists():

                for esp in datarequest.keys():


                    plantData = PlantData()
                    plantData.DeviceId =        datarequest[esp]['DeviceId']                    
                    plantData.SystemId =        datarequest[esp]['SystemId']
                    plantData.Temperature =     datarequest[esp]['Temperature']                   
                    plantData.Humidity =        datarequest[esp]['Humidity']                    
                    plantData.SoilMoisture =    datarequest[esp]['SoilMoisture']                   
                    plantData.Luminosity =      datarequest[esp]['Luminosity']
                    plantData.White_pic =       request.FILES['white_pic']
                    plantData.Nir_pic =         request.FILES['nir_pic']
                    plantData.VPD =             VPD.VPD.calcvpd(float(datarequest[esp]['Temperature']), float(datarequest[esp]['Humidity']))

                    plantData.save()


                ndvi = process.main(settings.BASE_DIR + "/polls" + plantData.White_pic.url, settings.BASE_DIR + "/polls" + plantData.Nir_pic.url, plantData.DeviceId, plantData.ServerTime)              
                plantData.NDVI_value = ndvi

                plantData.save()

                print('ESP: ' + datarequest[esp]['DeviceId'] + ' - RASP:' + datarequest[esp]['SystemId'] + ' - NDVI:' + str(ndvi))
                return HttpResponse('200' + ' - ESP: ' + datarequest[esp]['DeviceId'] + ' - RASP:' + datarequest[esp]['SystemId'] + ' - NDVI:' + str(ndvi))
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
        time_threshold = timezone.now() - timedelta(hours=2)
        plantswithdata = []

        for plant in plants:
            if PlantData.objects.filter(DeviceId=plant.deviceid).exists():

                #Latest row of plantdata for this plant sorted by ServerTime
                datarow = PlantData.objects.filter(DeviceId=plant.deviceid).latest('ServerTime')

                #Status:
                # 0 equals Good, no problems
                # 1 equals VPD problem
                # 2 equals problem with database or RASP connection

                problem, status, explanation, instructions = VPD.VPD.vpdAnalysis(datarow.Humidity, datarow.Temperature)

                if datarow.ServerTime < time_threshold:
                    plantswithdata.append([plant, datarow, "2", "DB problem"])
                elif problem: #If VPD analysis returns problematic values
                    plantswithdata.append([plant, datarow, "1", status + explanation + instructions])
                else:
                    plantswithdata.append([plant, datarow, "0", "Status OK"])

            else:
                plantswithdata.append([plant, "2", None, "DB"])

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
