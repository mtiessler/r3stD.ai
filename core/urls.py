from django.urls import path
from . import views

urlpatterns = [
    path('tryout', views.home),
    path('upload', views.upload)
]
