from django.urls import path
from main.backend import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recommender', views.recApp, name="recApp"),
    path('about', views.about, name="about")
]