from django.urls import path
from main.backend import views
from main.backend import gainers_losers_scrape

urlpatterns = [
    path('', views.home, name='home'),
    path('recommender', views.recApp, name="recApp"),
    path('about', views.about, name="about"),
    path('results', views.results, name="results"),
    path('ticker', views.tickers, name="tickers"),
    path('historical', views.historical, name="historical"),
    path('gainers', gainers_losers_scrape.gainers, name="gainers"),
    path('losers', gainers_losers_scrape.losers, name="losers"),
]