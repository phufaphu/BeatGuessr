from django.db import models
from django.contrib.auth.models import User

class Artist(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class Album(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')

    def __str__(self):
        return f"{self.title} by {self.artist.name}"

class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='songs')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs')
    youtube_url = models.URLField(unique=True)
    snippet_file = models.FileField(upload_to='clips/')

    def __str__(self):
        return self.title

class Playlist(models.Model):
    name = models.CharField(max_length=200)
    songs = models.ManyToManyField(Song, related_name='playlists')
    description = models.TextField(blank=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='added_playlists')

    def __str__(self):
        return self.name

class Game(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games')
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='games')
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Game {self.id} on '{self.playlist.name}' by {self.player.username}"

class GameRound(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='rounds')
    correct_song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='correct_in_rounds')
    choices = models.ManyToManyField(Song, related_name='choices_in_rounds')
    user_choice = models.ForeignKey(Song, on_delete=models.SET_NULL, null=True, blank=True, related_name='chosen_in_rounds')
    is_correct = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"Round for Game {self.game.id} - Song: {self.correct_song.title}"