from django.db import models
from django.conf.urls import url
from django.conf.urls import include
from django.urls import path, include
from django.contrib import admin
from polls.views import HomeView, display, addplant, myplants, postdata
from polls.views import frontpage
from polls import views
from django.contrib.auth.decorators import login_required



urlpatterns = [
    path('', include('customuser.urls', namespace='customuser')),
    path('admin/', admin.site.urls, name="admin"),
    path('', frontpage, name='frontpage'),
    path('myplants/', myplants, name='myplants'),
	path('addplant/', addplant, name='addplant'),
	path('myplants/<id>', display, name='display'),
    path('postdata/', postdata, name='display')

]