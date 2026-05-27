from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    
    # Artist URLs
    path('artists/', views.artist_list, name='artist_list'),
    path('artists/new/', views.artist_create, name='artist_create'),
    path('artists/<int:pk>/edit/', views.artist_update, name='artist_update'),
    path('artists/<int:pk>/delete/', views.artist_delete, name='artist_delete'),
    
    # Song URLs
    path('songs/', views.song_list, name='song_list'),
    path('songs/new/', views.song_create, name='song_create'),
    
    # Playlist URLs
    path('playlists/', views.playlist_list, name='playlist_list'),
    path('playlists/new/', views.playlist_create, name='playlist_create'),
]
