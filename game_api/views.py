import random
from django.shortcuts import get_object_or_404
from django.db import transaction

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Song, Playlist, Game, GameRound, User
from .serializers import (
    GameStateOutSerializer, GameStartSerializer,
    GuessResultSerializer, GuessSerializer
)

def generate_choices(correct_song: Song, all_songs: list) -> list:
    """Helper function to create 4 multiple choices. (ยกมาจากของเดิมได้เลย)"""
    choices = [correct_song]
    wrong_options = [s for s in all_songs if s.id != correct_song.id]
    choices.extend(random.sample(wrong_options, min(3, len(wrong_options))))
    random.shuffle(choices)
    return choices

class GameViewSet(viewsets.ViewSet):
    """
    A ViewSet for controlling the game flow.
    """

    @action(detail=False, methods=['post'], url_path='start')
    def start_game(self, request):
        serializer = GameStartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        playlist_id = serializer.validated_data['playlist_id']

        playlist = get_object_or_404(Playlist, id=playlist_id)
        all_songs_in_playlist = list(playlist.songs.all())

        if len(all_songs_in_playlist) < 4:
            return Response({"detail": "Playlist needs at least 4 songs."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            game_songs = random.sample(all_songs_in_playlist, min(10, len(all_songs_in_playlist)))
            player, _ = User.objects.get_or_create(username='testplayer')
            game = Game.objects.create(player=player, playlist=playlist)
            for song in game_songs:
                GameRound.objects.create(game=game, correct_song=song)

        first_round = game.rounds.first()
        choices = generate_choices(first_round.correct_song, all_songs_in_playlist)
        
        response_data = {
            "game_id": game.id,
            "score": game.score,
            "current_round": {
                "round_id": first_round.id,
                "snippet_url": request.build_absolute_uri(first_round.correct_song.snippet_file.url),
                "choices": choices
            }
        }
        
        response_serializer = GameStateOutSerializer(instance=response_data)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='guess')
    def submit_guess(self, request):
        serializer = GuessSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        with transaction.atomic():
            game = get_object_or_404(Game, id=data['game_id'], is_complete=False)
            current_round = get_object_or_404(GameRound, id=data['round_id'], game=game)
            user_choice = get_object_or_404(Song, id=data['choice_id'])

            if current_round.user_choice is not None:
                return Response({"detail": "This round has already been answered."}, status=status.HTTP_400_BAD_REQUEST)

            is_correct = (current_round.correct_song.id == user_choice.id)
            current_round.user_choice = user_choice
            current_round.is_correct = is_correct
            current_round.save()

            if is_correct:
                game.score += 10
                game.save()

            next_round_obj = GameRound.objects.filter(game=game, user_choice__isnull=True).first()
            
            next_round_data = None
            is_game_over = True
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
            
            response_data = {
                "is_correct": is_correct,
                "correct_song_id": current_round.correct_song.id,
                "new_score": game.score,
                "next_round": next_round_data,
                "is_game_over": is_game_over
            }
        
        response_serializer = GuessResultSerializer(instance=response_data)
        return Response(response_serializer.data, status=status.HTTP_200_OK)