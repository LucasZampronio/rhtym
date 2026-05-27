from django.contrib import admin
from .models import Artist, Song, Playlist, UserProfile

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'genre', 'has_image')
    
    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = "Foto?"

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'duration', 'has_audio', 'has_cover')
    
    def has_audio(self, obj):
        return bool(obj.audio_file)
    has_audio.boolean = True
    has_audio.short_description = "Áudio?"

    def has_cover(self, obj):
        return bool(obj.cover_image)
    has_cover.boolean = True
    has_cover.short_description = "Capa?"

admin.site.register(Playlist)
admin.site.register(UserProfile)
