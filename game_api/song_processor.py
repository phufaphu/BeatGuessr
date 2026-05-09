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
        # 🛡️ Extract Video ID robustly
        import re
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
            r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})',
            r'(?:embed\/)([0-9A-Za-z_-]{11})',
        ]
        
        video_id = None
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                video_id = match.group(1)
                break
        
        if not video_id:
            print(f"Could not extract video ID from {url}")
            return None
        temp_file_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp3")
        
        import shutil
        node_path = shutil.which('node')
        if not node_path:
            # Fallback search for common Node.js installations on macOS
            for path in ['/opt/homebrew/bin/node', '/usr/local/bin/node']:
                if os.path.exists(path):
                    node_path = path
                    break
        
        import yt_dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(DOWNLOAD_DIR, video_id),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'noplaylist': True,
            'quiet': True,
        }
        
        if node_path:
            ydl_opts['js_runtimes'] = {
                'node': {'path': node_path}
            }
            ydl_opts['remote_components'] = ['ejs:github']
            
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
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