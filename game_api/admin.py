from django.contrib import admin
from .models import Artist, Album, Song, Playlist, Game, GameRound

admin.site.register(Artist)
admin.site.register(Album)

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'artist', 'album', 'youtube_url')
    search_fields = ('title', 'artist__name')
    list_filter = ('artist', 'album')

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'song_count')
    search_fields = ('name',)
    filter_horizontal = ('songs',)

    @admin.display(description='Number of Songs')
    def song_count(self, obj):
        return obj.songs.count()

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'player', 'playlist', 'score', 'created_at', 'is_complete')
    list_filter = ('is_complete', 'playlist', 'player')

@admin.register(GameRound)
class GameRoundAdmin(admin.ModelAdmin):
    list_display = ('id', 'game', 'correct_song', 'user_choice', 'is_correct')
    list_filter = ('game', 'is_correct')