from django.urls import path
from . import views

urlpatterns = [
    path('novel/result', views.novel_analysis),
    path('text/result', views.text_analysis),
]
