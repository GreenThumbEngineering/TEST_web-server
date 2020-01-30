from django.db import models
from django.conf.urls import url
from django.conf.urls import include
from django.urls import path, include
from django.contrib import admin
from polls.views import HomeView
from polls.views import display
from polls.views import addplant
from polls.views import myplants
#from polls.views import displayplants
from polls.views import frontpage
from polls import views
from django.contrib.auth.decorators import login_required
#from .views import * 

app_name = 'dappx'

urlpatterns = [
    path('', include('customuser.urls', namespace='customuser')),
    path('admin/', admin.site.urls, name="admin"),
    path('', frontpage, name='frontpage'),
	#path('display/', display, name='display'),
    path('myplants/', myplants, name='myplants'),
	path('addplant/', addplant, name='addplant'),
	path('myplants/<id>', display, name='display')
    #url(r'^$',views.index,name='index'),
    #url(r'^special/',views.special,name='special'),
    #url(r'^dappx/',include('polls.urls')),
    #url(r'^logout/$', views.user_logout, name='logout'),
    #url(r'^dappx/user_login/planttemplate.html', display, name='display'),
]