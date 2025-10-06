from rest_framework import serializers
from .models import Song, Artist

# --- OUTPUT SERIALIZERS ---
class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['name']

class SongChoiceSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(source='artist.name')
    
    class Meta:
        model = Song
        fields = ['id', 'title', 'artist_name']

class GameRoundOutSerializer(serializers.Serializer):
    round_id = serializers.IntegerField()
    snippet_url = serializers.CharField()
    choices = SongChoiceSerializer(many=True)

class GameStateOutSerializer(serializers.Serializer):
    game_id = serializers.IntegerField()
    score = serializers.IntegerField()
    current_round = GameRoundOutSerializer()

class GuessResultSerializer(serializers.Serializer):
    is_correct = serializers.BooleanField()
    correct_song_id = serializers.IntegerField()
    new_score = serializers.IntegerField()
    next_round = GameRoundOutSerializer(allow_null=True)
    is_game_over = serializers.BooleanField()

# --- INPUT SERIALIZERS ---
class GameStartSerializer(serializers.Serializer):
    playlist_id = serializers.IntegerField(required=True)

class GuessSerializer(serializers.Serializer):
    game_id = serializers.IntegerField(required=True)
    round_id = serializers.IntegerField(required=True)
    choice_id = serializers.IntegerField(required=True)