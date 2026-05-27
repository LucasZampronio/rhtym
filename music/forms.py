from django import forms
from .models import Artist, Song, Playlist

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'genre', 'bio']

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'duration', 'artist', 'release_date']

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name', 'songs']
