from ninja import NinjaAPI
from typing import List
from .models import Playlist, Song
from .schemas import PlaylistSchema, PlaylistDetailSchema
api = NinjaAPI()

@api.get("/playlists", response=List[PlaylistSchema])
def list_playlists(request):
    """
    Returns a list of all available playlists in the system.
    """
    playlists = Playlist.objects.all()
    return playlists

@api.get("/playlists/{playlist_id}", response=PlaylistDetailSchema)
def get_playlist_details(request, playlist_id: int):
    """
    Returns the details for a single playlist, including a list of its songs.
    """
    playlist = Playlist.objects.prefetch_related('songs').get(id=playlist_id)
    return playlist