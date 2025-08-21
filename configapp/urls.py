from django.contrib import admin
from django.urls import path
from configapp.views import *

urlpatterns = [
    path('', index, name="home"),
    path('add_salon/', add_salon, name="add_salon"),
    path('detail_salon/<int:pk>/', detail_salon, name='detail_salon'),
    path('salon_cars/<int:brand_pk>/<int:salon_pk>/', salon_cars, name='salon_cars'),
    path('add_car/', add_car, name='add_car'),

    path('car/<int:pk>/', car_detail, name='car_detail'),
    path('car/<int:car_id>/pdf/', detailed_pdf, name='car_pdf'),
]


