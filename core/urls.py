from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.upload),
    path('', views.home, name='home'),
    path('aboutUs', views.about, name='aboutus'),
    path('documentation', views.docs, name='docs'),
    path('results', views.results, name='results')
]
