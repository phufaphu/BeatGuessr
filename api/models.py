from django.db import models
from django.contrib.auth.models import User

# --- Core Music Models ---

class Artist(models.Model):
    """Represents a music artist."""
    name = models.CharField(max_length=200, unique=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Album(models.Model):
    """Represents an album released by an Artist."""
    title = models.CharField(max_length=200)
    release_date = models.DateField()
    cover_art_url = models.URLField(max_length=500)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')

    def __str__(self):
        return f"{self.title} by {self.artist.name}"

class Song(models.Model):
    """Represents a single song from an Album."""
    title = models.CharField(max_length=200)
    duration_seconds = models.IntegerField()
    audio_preview_url = models.URLField(max_length=500, unique=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs')

    def __str__(self):
        return f"{self.title} ({self.album.title})"

# --- Game Logic Models ---

class Playlist(models.Model):
    """Represents a themed collection of songs for a game mode."""
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    songs = models.ManyToManyField(Song, related_name='playlists')

    def __str__(self):
        return self.name

class Game(models.Model):
    """Represents a single gameplay session for a User."""
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games')
    playlist = models.ForeignKey(Playlist, on_delete=models.SET_NULL, null=True, blank=True, related_name='games')

    def __str__(self):
        return f"Game for {self.user.username} (Score: {self.score})"

class Guess(models.Model):
    """Represents a user's guess for a specific song within a game session."""
    user_answer = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='guesses')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='guesses')

    def __str__(self):
        return f"Guess by {self.game.user.username} for '{self.song.title}' - Correct: {self.is_correct}"