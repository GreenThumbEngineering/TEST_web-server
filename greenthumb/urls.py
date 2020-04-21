from django.db import models
from polls import views
from django.conf.urls import url, include
from django.urls import path, include
from django.contrib import admin
from polls.views import display, addplant, myplants, postdata, frontpage, PlantUpdate, PlantDataUpdate, odfread
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include('customuser.urls', namespace='customuser')),
    path('admin/', admin.site.urls, name="admin"),
    path('', frontpage, name='frontpage'),
    path('myplants/', myplants, name='myplants'),
	path('addplant/', addplant, name='addplant'),
	path('myplants/<id>', display, name='display'),
    path('postdata/', postdata, name='postdata'),
    path('grade/', PlantDataUpdate.as_view(), name='grade'),
    path('myplants/<pk>/update/', PlantUpdate.as_view(), name='plantupdate'),
    path('odfread/',odfread, name='odfread')
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)