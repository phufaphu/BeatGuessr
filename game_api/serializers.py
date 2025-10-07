from rest_framework import serializers
from .models import Song, Artist, User, Game, Playlist

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

# --- USER SERIALIZERS ---
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class SimplePlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['id', 'name']

class GameHistorySerializer(serializers.ModelSerializer):
    playlist = SimplePlaylistSerializer(read_only=True)
    
    class Meta:
        model = Game
        fields = ['id', 'score', 'created_at', 'is_complete', 'playlist']