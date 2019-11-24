# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Book
from .models import PlantData
from django.shortcuts import render_to_response
from django.utils.datastructures import MultiValueDictKeyError
from polls import connect


def frontpage(request):
		return render(request, 'index.html')


def display321(request):
		try:
			increment = int(request.GET['append_increment'])
			increment_to = increment + 10
			return render_to_response('get_values.html', {'obj': Book.objects.all().order_by('publication_year')[:5]})
		except:
			increment = 0
			increment_to = increment + 10
			return render_to_response('template.html', {'obj': Book.objects.all().order_by('publication_year')[:5]})
			
def display(request):
		try:
			#increment = int(request.GET['append_increment'])			
			return render_to_response('get_plant_values.html', {'obj': connect.getData()})
		except:
			#increment = 0			
			return render_to_response('planttemplate.html', {'obj': connect.getData()})	

			
#def displayplants(request):
#		try:
#			increment = int(request.GET['append_increment'])			
#			return render_to_response('get_plant_values.html', {'obj': PlantData.objects.all().order_by('-id')[:20]})
#		except:
#			increment = 0			
#			return render_to_response('planttemplate.html', {'obj': PlantData.objects.all().order_by('-id')[:20]})			


class HomeView(TemplateView):
    template_name = 'index.html'
		
