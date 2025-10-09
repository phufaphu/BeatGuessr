from django.contrib import admin
from django.db.models import Count
from .models import Artist, Album, Song, Playlist, Game, GameRound

# --- Inline Admin Classes ---
class SongInline(admin.TabularInline):
    """Allows editing Songs from the Album page."""
    model = Song
    extra = 1
    fields = ('title', 'youtube_url', 'snippet_file')
    readonly_fields = ('snippet_file',)

# --- Main Admin Classes ---

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'album_count', 'song_count')
    search_fields = ('name',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _album_count=Count("albums", distinct=True),
            _song_count=Count("songs", distinct=True),
        )
        return queryset

    def album_count(self, obj):
        return obj._album_count

    def song_count(self, obj):
        return obj._song_count

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'song_count')
    list_filter = ('artist',)
    search_fields = ('title', 'artist__name')
    inlines = [SongInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(_song_count=Count("songs"))
        return queryset

    def song_count(self, obj):
        return obj._song_count

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'album', 'youtube_url')
    search_fields = ('title', 'artist__name', 'album__title')
    list_filter = ('artist', 'album')
    autocomplete_fields = ['artist', 'album']

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'song_count')
    search_fields = ('name',)
    filter_horizontal = ('songs',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(_song_count=Count("songs"))
        return queryset

    @admin.display(description='Number of Songs')
    def song_count(self, obj):
        return obj._song_count

# --- Game History Admins ---

class GameRoundInline(admin.TabularInline):
    model = GameRound
    extra = 0
    can_delete = False
    readonly_fields = ('correct_song', 'user_choice', 'is_correct')
    
    def has_add_permission(self, request, obj=None):
        return False

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'player', 'playlist', 'score', 'created_at', 'is_complete')
    list_filter = ('is_complete', 'playlist', 'player')
    search_fields = ('player__username',)
    readonly_fields = ('player', 'playlist', 'score', 'created_at', 'is_complete')
    inlines = [GameRoundInline]