from django.urls import path
from . import views

urlpatterns = [
    path('search_movies/', views.scrape_main, name='data'),
    path('Netflix_movies/', views.Netflix_Movie, name='Netflix'),
    path('All_movies/', views.All_Movies, name='movie'),
    path('Movies_Data/', views.scrape_movies_data, name='scrape_rotten_tomatoes'),


    # Actors
    path('actor/', views.ActorAPIView.as_view(), name='actor_api'),
    path('acotrss/', views.ActorsDetail.as_view(), name='scrape_api'),
    path('Popular_actors/', views.Popular_actors, name='data'),

    # Netflix
    path('Top_Netflix_movies/', views.Top_Netflix_Movie, name='Top_Netflix_movies'),

    # Upcoming Movies
    path('new_movies/', views.get_upcoming_movies, name='new_movies'),
    path('Upcoming_movies/', views.Upcoming_Movies, name='Upcoming'),

    # New Movies
    path('New_movies_data/', views.New_Movies, name='new_movies'),

    # Upcoming Season
    path('Upcoming_seasons_data/', views.get_upcoming_season, name=''),
    path('Tv_Shows/', views.Season_tv_shows, name='TV Shows'),

    # New Season
    path('New_seasons_data/', views.new_seasons, name='new_season'),





    # Netflix Movies/Seasons
    path('Netflix_movies_data/', views.Netflix_upcoming_movies, name='Netflix_movies'),
    path('Netflix_New_Movies_data/', views.Netflix_New_Movies, name='Netflix_new_movies'),
    path('Netflix_seasons_data/', views.Netflix_upcoming_season, name='Netflix_Upcoming_seasons'),
    path('Netflix_new_Season_data/', views.Netflix_new_seasons, name='Netflix_new_Season'),
    path('Top_Netflix_seasons/', views.Top_Netflix_Season, name=''),


    # Hulu Movies/Seasons
    path('Hulu_movies_data/', views.Hulu_Movies_data, name='Hulu_movies'),
    path('Hulu_New_movies_data/', views.Hulu_New_Movies, name='Hulu_new_movies'),
    path('Hulu_season_data/', views.Hulu_season_data, name='Hulu_season'),
    path('Hulu_New_season_data/', views.Hulu_new_seasons, name='Hulu_new_season'),


    # Amazon Prime Movies/Seasons
    path('PrimeVideo_movies_data/', views.AmazonPrime_Movies_data, name='PrimeVideo_movies'),
    path('AmazonPrime_New_movies_data/', views.AmazonPrime_New_Movies, name='Hulu_new_movies'),
    path('AmazonPrime_season_data/', views.AmazonPrime_season_data, name='Hulu_season'),
    path('AmazonPrime_New_season_data/', views.AmazonPrime_new_seasons, name='Hulu_new_season'),



]
