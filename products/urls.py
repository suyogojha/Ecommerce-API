
from django.urls import path
from .views import *


app_name = 'products'

urlpatterns = [
    path('products/', ProductView.as_view()),
    path('demo/', DemoView.as_view()),
]
