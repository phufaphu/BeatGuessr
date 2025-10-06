from django.contrib import admin
from .models import Artist, Album, Song, Playlist

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