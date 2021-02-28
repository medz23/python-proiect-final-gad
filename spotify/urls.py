from django.urls import path
from . import views
from .views import AuthURL, spotify_callback, IsAuthenticated

app_name = "spotify"

urlpatterns = [
    path('', views.photolinks, name='photos'),
    path('search-song', views.searchsong, name='search_song'),
    path('get-auth-url', AuthURL.as_view(), name='connect'),
    path('redirect', spotify_callback, name='redirect'),
    path('is-authenticated', IsAuthenticated.as_view(), name='authenticated'),
]
 # "url": "https://accounts.spotify.com/authorize?scope=user-read-playback-state+user-modify-playback-state+user-read-currently-playing&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fspotify%2Fredirect&client_id=08cb230a331944c7bfa503dfc73dd46c"
