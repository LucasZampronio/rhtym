from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# Requisito: Pelo menos 1 classe que utilize os conceitos de enumerations.
class SubscriptionType(models.TextChoices):
    FREE = 'FR', 'Free'
    PREMIUM = 'PR', 'Premium'
    ARTIST = 'AR', 'Artista'

# Requisito: Pelo menos 4 modelos principais.
# Modelo 1: Artist
class Artist(models.Model):
    name = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='artists/', null=True, blank=True)

    def __str__(self):
        return self.name

# Requisito: Pelo menos 1 manager personalizado ou método de consulta reutilizável.
class SongManager(models.Manager):
    def get_by_title(self, title):
        return self.filter(title__icontains=title)

# Modelo 2: Song
class Song(models.Model):
    title = models.CharField(max_length=200)
    duration = models.DurationField()
    audio_file = models.FileField(upload_to='songs/', null=True, blank=True)
    cover_image = models.ImageField(upload_to='covers/', null=True, blank=True)
    # Requisito: Pelo menos 2 relacionamentos entre os modelos. (1/2)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='songs')
    release_date = models.DateField()
    
    objects = SongManager()

    # Requisito: Pelo menos 3 validações personalizadas. (1/3)
    def clean(self):
        if len(self.title) < 2:
            raise ValidationError("O título da música deve ter pelo menos 2 caracteres.")
        super().clean()

    def __str__(self):
        return f"{self.title} - {self.artist.name}"

# Modelo 3: Playlist
class Playlist(models.Model):
    name = models.CharField(max_length=100)
    # Requisito: Pelo menos 2 relacionamentos entre os modelos. (2/2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    # ManyToMany é um relacionamento
    songs = models.ManyToManyField(Song, related_name='playlists')

    # Requisito: Pelo menos 3 validações personalizadas. (2/3)
    def clean(self):
        if "proibido" in self.name.lower():
            raise ValidationError("O nome da playlist não pode conter a palavra 'proibido'.")
        super().clean()

    def __str__(self):
        return f"{self.name} ({self.user.username})"

# Modelo 4: UserProfile (Extensão do User)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    subscription = models.CharField(
        max_length=2,
        choices=SubscriptionType.choices,
        default=SubscriptionType.FREE
    )
    birth_date = models.DateField(null=True, blank=True)

    # Requisito: Pelo menos 3 validações personalizadas. (3/3)
    def clean(self):
        if self.birth_date and self.birth_date.year < 1900:
            raise ValidationError("Data de nascimento inválida.")
        super().clean()

    def __str__(self):
        return f"{self.user.username} - {self.get_subscription_display()}"
