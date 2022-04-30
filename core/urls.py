from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.upload),
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('documentation', views.docs, name='docs'),
    path('results', views.results, name='results')
]
