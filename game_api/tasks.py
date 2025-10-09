from celery import shared_task
import yt_dlp
from .song_processor import process_youtube_url
from .models import Playlist
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@shared_task
def import_youtube_playlist(playlist_id: int, youtube_playlist_url: str):
    print(f"Starting import for Playlist ID: {playlist_id} from URL: {youtube_playlist_url}")
    send_log(playlist_id, "Import task started...")
    
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
    send_log(playlist_id, f"Found {total_videos} videos in the playlist.")

    for index, video in enumerate(video_entries):
        video_url = f"https://www.youtube.com/watch?v={video['id']}"
        title = video.get('title', 'Unknown Title')
        artist = video.get('uploader', 'Unknown Artist')
        
        print(f"({index+1}/{total_videos}) Processing: {title}")
        send_log(playlist_id, f"({index+1}/{total_videos}) Downloading: {title}...")

        song_obj = process_youtube_url(
            url=video_url,
            title=title,
            artist_name=artist
        )
        
        if song_obj:
            playlist.songs.add(song_obj)
            send_log(playlist_id, f"   -> Successfully processed and added '{title}'.")
        else:
            send_log(playlist_id, f"   -> FAILED to process '{title}'.")
    
    print(f"Finished import for Playlist ID: {playlist_id}")
    send_log(playlist_id, "Import finished! You can now refresh the page.")
    return f"Successfully imported {len(video_entries)} songs."

def send_log(playlist_id, message):
    channel_layer = get_channel_layer()
    group_name = f'import_logs_{playlist_id}'
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_log_message',
            'message': message
        }
    )