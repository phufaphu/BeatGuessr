from ninja import Schema
from typing import List

class ArtistSchema(Schema):
    id: int
    name: str

class SongSchema(Schema):
    id: int
    title: str
    audio_preview_url: str

class AlbumSchema(Schema):
    id: int
    title: str
    cover_art_url: str
    artist: ArtistSchema

class PlaylistSchema(Schema):
    id: int
    name: str
    description: str

class PlaylistDetailSchema(Schema):
    id: int
    name: str
    description: str
    songs: List[SongSchema]