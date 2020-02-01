from django.db import models
from polls import views
from django.conf.urls import url, include
from django.urls import path, include
from django.contrib import admin
from polls.views import display, addplant, myplants, postdata, frontpage
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', include('customuser.urls', namespace='customuser')),
    path('admin/', admin.site.urls, name="admin"),
    path('', frontpage, name='frontpage'),
    path('myplants/', myplants, name='myplants'),
	path('addplant/', addplant, name='addplant'),
	path('myplants/<id>', display, name='display'),
    path('postdata/', postdata, name='postdata')

]