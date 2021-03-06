"""movie_watchtime URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api.views import auth, movies, user, watchlist

urlpatterns = [
    path("admin/", admin.site.urls),
    path("v1/auth/register/", auth.RegisterView.as_view()),
    path("v1/auth/login/", auth.LoginView.as_view()),
    path("v1/movies/list", movies.MoviesList.as_view()),
    path("v1/movies/detail/<int:movie_id>", movies.MovieDetail.as_view()),
    path("v1/movies/ingest/", movies.IngestMovie.as_view()),
    path("v1/user/movie/history", user.UserMovieHistory.as_view()),
    path("v1/user/add/movie/", user.AddMovieToAlreadyWatchList.as_view()),
    path("v1/user/watchlist/history", watchlist.UserWatchlistHistory.as_view()),
    path("v1/user/add/watchlist/", watchlist.AddMovieToWatchList.as_view()),
    path("v1/user/stats", user.UserDashboardStats.as_view()),
]
