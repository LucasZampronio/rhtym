from django.contrib import admin
from .models import Artist, Song, Playlist, UserProfile

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'genre')

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'duration', 'has_audio')
    
    def has_audio(self, obj):
        return bool(user_audio := obj.audio_file)
    has_audio.boolean = True
    has_audio.short_description = "Possui Áudio?"

admin.site.register(Playlist)
admin.site.register(UserProfile)
