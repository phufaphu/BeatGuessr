import random
from ninja import NinjaAPI, Schema
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from .models import Game, GameRound, Song, Album, Artist, Playlist

api = NinjaAPI()

# --- Schemas ---
class ArtistSchema(Schema):
    name: str

class SongChoiceSchema(Schema):
    id: int
    title: str
    artist_name: str

class GameRoundOutSchema(Schema):
    snippet_url: str 
    choices: list[SongChoiceSchema]

class GameStateOutSchema(Schema):
    game_id: int
    score: int
    current_round: GameRoundOutSchema

class GameStartSchema(Schema):
    playlist_id: int


# --- API Endpoint ---
@api.post("/game/start")
def start_game(request):
    all_songs = list(Song.objects.all())
    
    if len(all_songs) < 4:
        return api.create_response(request, {"detail": "Not enough songs in the database to start a game."}, status=400)

    game_songs = random.sample(all_songs, min(10, len(all_songs)))
    
    correct_song = game_songs[0]
    choices = [correct_song]
    wrong_options = [s for s in all_songs if s.id != correct_song.id]
    choices.extend(random.sample(wrong_options, 3))
    random.shuffle(choices)

    first_round_data = {
        "snippet_url": request.build_absolute_uri(correct_song.snippet_file.url),
        "choices": [
            {"id": c.id, "title": c.title, "artist_name": c.artist.name}
            for c in choices
        ]
    }
    
    return {"current_round": first_round_data}