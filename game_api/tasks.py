from celery import shared_task
import yt_dlp
from .song_processor import process_youtube_url
from .models import Playlist

@shared_task
def import_youtube_playlist(playlist_id: int, youtube_playlist_url: str):
    print(f"Starting import for Playlist ID: {playlist_id} from URL: {youtube_playlist_url}")
    
    try:
        playlist = Playlist.objects.get(id=playlist_id)
    except Playlist.DoesNotExist:
        print(f"Playlist ID: {playlist_id} not found. Aborting task.")
        return

    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
    }
    
    video_entries = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            playlist_dict = ydl.extract_info(youtube_playlist_url, download=False)
            video_entries = playlist_dict['entries']
        except Exception as e:
            print(f"Failed to extract playlist info: {e}")
            return

    total_videos = len(video_entries)
    print(f"Found {total_videos} videos in the playlist.")

    for index, video in enumerate(video_entries):
        video_url = f"https://www.youtube.com/watch?v={video['id']}"
        title = video.get('title', 'Unknown Title')
        artist = video.get('uploader', 'Unknown Artist')
        
        print(f"({index+1}/{total_videos}) Processing: {title}")

        song_obj = process_youtube_url(
            url=video_url,
            title=title,
            artist_name=artist
        )
        
        if song_obj:
            playlist.songs.add(song_obj)
    
    print(f"Finished import for Playlist ID: {playlist_id}")
    return f"Successfully imported {len(video_entries)} songs."