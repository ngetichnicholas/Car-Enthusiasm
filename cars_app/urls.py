from django.urls import path
from cars_app import views as app_view

urlpatterns = [
    path('',app_view.index,name='index'),

]