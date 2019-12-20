from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Book
from .models import PlantData
from .models import Plants
from django.utils.datastructures import MultiValueDictKeyError
from polls import connect


def frontpage(request):
		return render(request, 'index.html')
			
def display(request):		
		return render('planttemplate.html', {'obj': connect.getData()})

def addplant(request):
	if request.method == 'POST':
		if request.POST.get('userid') and request.POST.get('nickname') and request.POST.get('deviceid'):
			plant = Plants()
			plant.userid = request.POST.get('userid')
			plant.nickname = request.POST.get('nickname')
			plant.deviceid = request.POST.get('deviceid')
			plant.save()

			return render(request, 'addplant.html')
	else:
		return render(request, 'addplant.html')

class HomeView(TemplateView):
    template_name = 'index.html'
