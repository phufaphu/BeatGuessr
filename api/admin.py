from django.contrib import admin
from api.models import Artist, Album, Song, Playlist, Game, Guess

# Register your models here.
admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Playlist)
admin.site.register(Game)
admin.site.register(Guess)
