from django.contrib import admin
from django.urls import path,include
from .views import Databundle,Airtime,ResultView,Electricity,CableView,BetView
urlpatterns = [

    path('airtime/', Airtime.as_view()),
    path('data/', Databundle.as_view()),
    path('bills/', Electricity.as_view()),
    path('bills/<str:status>/<str:billerslug>', Electricity.as_view()),
    path('cable/', CableView.as_view()),
    path('cable/<str:status>/<str:billerslug>', CableView.as_view()),
    path('bet/', BetView.as_view()),
    path('bet/<str:status>/<str:billerslug>', BetView.as_view()),
    path('result/', ResultView.as_view()),

]