import os
import random
import subprocess
from pydub import AudioSegment
from django.conf import settings
from .models import Song, Artist, Album

DOWNLOAD_DIR = os.path.join(settings.BASE_DIR, "temp_downloads")
CLIPS_DIR = os.path.join(settings.MEDIA_ROOT, "clips")

def process_youtube_url(url: str, title: str, artist_name: str):
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    os.makedirs(CLIPS_DIR, exist_ok=True)

    existing_song = Song.objects.filter(youtube_url=url).first()
    if existing_song:
        print(f"Song '{title}' already exists. Returning existing object.")
        return existing_song

    audio_file_path = download_audio(url)
    if not audio_file_path:
        return None

    snippet_db_path = make_snippet(audio_file_path)
    if not snippet_db_path:
        return None
    
    os.remove(audio_file_path)

    song_object = save_to_db(url, title, artist_name, snippet_db_path)
    return song_object

def download_audio(url: str):
    print(f"Downloading: {url}")
    try:
        video_id = url.split("v=")[-1].split("&")[0]
        temp_file_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp3")
        
        subprocess.run([
            "yt-dlp", "-x", "--audio-format", "mp3",
            "-o", temp_file_path,
            url
        ], check=True, capture_output=True)
        return temp_file_path
    except Exception as e:
        print(f"Failed to download {url}. Error: {e}")
        return None

def make_snippet(input_path: str):
    try:
        song = AudioSegment.from_file(input_path)
        duration_ms = len(song)
        if duration_ms < 15000:
            print(f"Skipping {input_path}: too short")
            return None, None

        start_ms = random.randint(0, duration_ms - 15000)
        snippet = song[start_ms : start_ms + 15000] # 15 seconds

        filename = os.path.basename(input_path).replace(".mp3", "_snippet.mp3")
        output_path = os.path.join(CLIPS_DIR, filename)
        snippet_db_path = os.path.join('clips', filename)
        
        snippet.export(output_path, format="mp3")
        print(f"  -> Created snippet: {snippet_db_path}")
        
        return snippet_db_path
    except Exception as e:
        print(f"Failed to create snippet. Error: {e}")
        return None

def save_to_db(url: str, title: str, artist_name: str, snippet_path: str):
    artist, _ = Artist.objects.get_or_create(name=artist_name)
    album, _ = Album.objects.get_or_create(title=title, artist=artist) # สมมติชื่ออัลบั้ม = ชื่อเพลง

    song = Song.objects.create(
        title=title,
        artist=artist,
        album=album,
        youtube_url=url,
        snippet_file=snippet_path
    )
    print(f"Saved '{title}' to database.")
    return song