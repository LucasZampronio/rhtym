from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Artist, Song, Playlist
from .forms import ArtistForm, SongForm, PlaylistForm

# Requisito: Autenticação, login, logout e controle de acesso.
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# Listagem (Consultas)
def index(request):
    songs = Song.objects.all()
    artists = Artist.objects.all()
    return render(request, 'music/index.html', {'songs': songs, 'artists': artists})

# --- ARTIST CRUD ---
def artist_list(request):
    artists = Artist.objects.all()
    return render(request, 'music/artist_list.html', {'artists': artists})

@login_required
def artist_create(request):
    if request.method == 'POST':
        form = ArtistForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('artist_list')
    else:
        form = ArtistForm()
    return render(request, 'music/form.html', {'form': form, 'title': 'Novo Artista'})

@login_required
def artist_update(request, pk):
    artist = get_object_or_404(Artist, pk=pk)
    if request.method == 'POST':
        form = ArtistForm(request.POST, request.FILES, instance=artist)
        if form.is_valid():
            form.save()
            return redirect('artist_list')
    else:
        form = ArtistForm(instance=artist)
    return render(request, 'music/form.html', {'form': form, 'title': 'Editar Artista'})

@login_required
def artist_delete(request, pk):
    artist = get_object_or_404(Artist, pk=pk)
    if request.method == 'POST':
        artist.delete()
        return redirect('artist_list')
    return render(request, 'music/confirm_delete.html', {'object': artist})

# --- SONG CRUD ---
def song_list(request):
    songs = Song.objects.all()
    return render(request, 'music/song_list.html', {'songs': songs})

@login_required
def song_create(request):
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('song_list')
    else:
        form = SongForm()
    return render(request, 'music/form.html', {'form': form, 'title': 'Nova Música'})

# --- PLAYLIST CRUD ---
@login_required
def playlist_list(request):
    playlists = Playlist.objects.filter(user=request.user)
    return render(request, 'music/playlist_list.html', {'playlists': playlists})

@login_required
def playlist_create(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.user = request.user
            playlist.save()
            form.save_m2m() # Importante para ManyToMany
            return redirect('playlist_list')
    else:
        form = PlaylistForm()
    return render(request, 'music/form.html', {'form': form, 'title': 'Nova Playlist'})
