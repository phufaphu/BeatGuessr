from rest_framework import serializers
from .models import Song, Artist, User, Game, Playlist, Album

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
        fields = ['id', 'username', 'email', 'is_staff']

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

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value

class AddSongSerializer(serializers.Serializer):
    youtube_url = serializers.URLField()
    title = serializers.CharField(max_length=200)
    artist = serializers.CharField(max_length=200)

class PlaylistDetailSerializer(serializers.ModelSerializer):
    songs = SongChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Playlist
        fields = ['id', 'name', 'songs']

class PlaylistWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['name']

class SongActionSerializer(serializers.Serializer):
    song_id = serializers.IntegerField(required=True)

class ImportPlaylistSerializer(serializers.Serializer):
    youtube_playlist_url = serializers.URLField()