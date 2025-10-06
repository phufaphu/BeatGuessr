import random
from ninja import NinjaAPI, Schema
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Song, Playlist, Game, GameRound
from django.contrib.auth.models import User
from typing import Optional

api = NinjaAPI()

# --- INPUT SCHEMAS ---
class GameStartSchema(Schema):
    playlist_id: int

class GuessSchema(Schema):
    game_id: int
    round_id: int
    choice_id: int

# --- OUTPUT SCHEMAS ---
class SongChoiceSchema(Schema):
    id: int
    title: str
    artist_name: str

class GameRoundOutSchema(Schema):
    round_id: int
    snippet_url: str
    choices: list[SongChoiceSchema]

class GameStateOutSchema(Schema):
    game_id: int
    score: int
    current_round: GameRoundOutSchema

class GuessResultSchema(Schema):
    is_correct: bool
    correct_song_id: int
    new_score: int
    next_round: Optional[GameRoundOutSchema] = None
    is_game_over: bool


# --- API Endpoint ---
@api.post("/game/start", response=GameStateOutSchema)
@transaction.atomic
def start_game(request, payload: GameStartSchema):
    playlist = get_object_or_404(Playlist, id=payload.playlist_id)
    all_songs_in_playlist = list(playlist.songs.all())

    if len(all_songs_in_playlist) < 4:
        return api.create_response(request, {"detail": "Playlist needs at least 4 songs."}, status=400)

    game_songs = random.sample(all_songs_in_playlist, min(10, len(all_songs_in_playlist)))
    
    player, _ = User.objects.get_or_create(username='testplayer')
    game = Game.objects.create(player=player, playlist=playlist)

    for song in game_songs:
        GameRound.objects.create(game=game, correct_song=song)

    first_round = game.rounds.first()
    choices = generate_choices(first_round.correct_song, all_songs_in_playlist)
    
    return {
        "game_id": game.id,
        "score": game.score,
        "current_round": {
            "round_id": first_round.id,
            "snippet_url": request.build_absolute_uri(first_round.correct_song.snippet_file.url),
            "choices": choices
        }
    }

@api.post("/game/guess", response=GuessResultSchema)
@transaction.atomic
def submit_guess(request, payload: GuessSchema):
    game = get_object_or_404(Game, id=payload.game_id, is_complete=False)
    current_round = get_object_or_404(GameRound, id=payload.round_id, game=game)
    user_choice = get_object_or_404(Song, id=payload.choice_id)

    if current_round.user_choice is not None:
        return api.create_response(request, {"detail": "This round has already been answered."}, status=400)

    is_correct = (current_round.correct_song.id == user_choice.id)
    
    current_round.user_choice = user_choice
    current_round.is_correct = is_correct
    current_round.save()

    if is_correct:
        game.score += 10
        game.save()

    next_round_obj = GameRound.objects.filter(game=game, user_choice__isnull=True).first()
    
    if next_round_obj:
        playlist_songs = list(game.playlist.songs.all())
        choices = generate_choices(next_round_obj.correct_song, playlist_songs)
        next_round_data = {
            "round_id": next_round_obj.id,
            "snippet_url": request.build_absolute_uri(next_round_obj.correct_song.snippet_file.url),
            "choices": choices
        }
        is_game_over = False
    else:
        game.is_complete = True
        game.save()
        next_round_data = None
        is_game_over = True

    return {
        "is_correct": is_correct,
        "correct_song_id": current_round.correct_song.id,
        "new_score": game.score,
        "next_round": next_round_data,
        "is_game_over": is_game_over
    }

def generate_choices(correct_song: Song, all_songs: list) -> list:
    """Helper function to create 4 multiple choices."""
    choices = [correct_song]
    wrong_options = [s for s in all_songs if s.id != correct_song.id]
    choices.extend(random.sample(wrong_options, min(3, len(wrong_options))))
    random.shuffle(choices)
    
    return [
        {"id": c.id, "title": c.title, "artist_name": c.artist.name}
        for c in choices
    ]