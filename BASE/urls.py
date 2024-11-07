from django.contrib import admin
from django.urls import path,include
from .views import *
urlpatterns = [
    path('',home,name='home'),
    path('owner_director_view/',owner_director_view,name='owner_director_view'),
    path('user_creation_owner/',user_creation_owner,name='user_creation_owner'),
    path('delete_user/<int:user_id>/',delete_user,name='delete_user'),
]