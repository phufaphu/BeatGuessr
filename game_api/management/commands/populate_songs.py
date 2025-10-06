import os
import random
import subprocess
from pydub import AudioSegment
from django.core.management.base import BaseCommand
from django.conf import settings
from game_api.models import Song, Artist, Album

SONG_CATALOG = [
    {'url': "https://www.youtube.com/watch?v=v7hts-62q3I", 'title': "บ้านพี่ปลอบ", 'artist': "Tattoo Colour"},
    {'url': "https://www.youtube.com/watch?v=-T_BCpTYJR8", 'title': "แล้วจะให้ไปรักใครได้อีก", 'artist': "Television Off"},
    {'url': "https://www.youtube.com/watch?v=k4vEgAsK3kg", 'title': "เหมือนโลกจะพัง", 'artist': "Dept"},
    {'url': "https://www.youtube.com/watch?v=GBAjOP33e4c", 'title': "ไม่เคยอ่อนแอแบบนี้มาก่อนเลย", 'artist': "Television Off"},
]

DOWNLOAD_DIR = os.path.join(settings.BASE_DIR, "temp_downloads")
CLIPS_DIR = os.path.join(settings.MEDIA_ROOT, "clips")

class Command(BaseCommand):
    help = 'Downloads songs from YouTube, creates snippets, and populates the database.'

    def handle(self, *args, **options):
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        os.makedirs(CLIPS_DIR, exist_ok=True)

        for song_data in SONG_CATALOG:
            url = song_data['url']

            # check if song already exists
            if Song.objects.filter(youtube_url=url).exists():
                self.stdout.write(self.style.WARNING(f"Skipping {song_data['title']}, already in database."))
                continue

            audio_file = self.download_audio(url)
            if audio_file:
                snippet_path_on_disk, snippet_db_path = self.make_snippet(audio_file)
                if snippet_path_on_disk:
                    self.save_to_db(song_data, snippet_db_path)
        
        self.stdout.write(self.style.SUCCESS('Finished populating songs.'))

    def download_audio(self, url):
        self.stdout.write(f"Downloading: {url}")
        try:
            video_id = url.split("v=")[1]
            temp_file_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp3")
            
            subprocess.run([
                "yt-dlp", "-x", "--audio-format", "mp3",
                "-o", temp_file_path,
                url
            ], check=True)
            return temp_file_path
        
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Failed to download {url}. Error: {e}"))
            return None

    def make_snippet(self, input_path):
        try:
            song = AudioSegment.from_file(input_path)
            duration_ms = len(song)
            if duration_ms < 15000:
                self.stdout.write(self.style.WARNING(f"Skipping {input_path}: too short"))
                return None, None

            start_ms = random.randint(0, duration_ms - 15000)
            snippet = song[start_ms : start_ms + 15000] # 15 seconds

            filename = os.path.basename(input_path).replace(".mp3", "_snippet.mp3")
            output_path_on_disk = os.path.join(CLIPS_DIR, filename)
            snippet_db_path = os.path.join('clips', filename)

            snippet.export(output_path_on_disk, format="mp3")
            self.stdout.write(f"  -> Created snippet: {snippet_db_path}")
            return output_path_on_disk, snippet_db_path
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Failed to create snippet for {input_path}. Error: {e}"))
            return None, None

    def save_to_db(self, song_data, snippet_db_path):
        artist, _ = Artist.objects.get_or_create(name=song_data['artist'])
        album, _ = Album.objects.get_or_create(title=song_data['title'], artist=artist)

        Song.objects.create(
            title=song_data['title'],
            artist=artist,
            album=album,
            youtube_url=song_data['url'],
            snippet_file=snippet_db_path
        )
        self.stdout.write(self.style.SUCCESS(f"  -> Saved '{song_data['title']}' to database."))