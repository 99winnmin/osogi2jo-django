from django.urls import path
from . import views

urlpatterns = [
    path('result', views.text_analysis),
]
