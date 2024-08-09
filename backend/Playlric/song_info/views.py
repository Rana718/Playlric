from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
import yt_dlp as youtube_dl
from .music_info import all_details
import re
import threading
import time
from django.conf import settings

@csrf_exempt
def search(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        query = data.get('query')

        if not query:
            return JsonResponse({'error': 'Query parameter is missing'}, status=400)

        try:
            video_data_list = all_details(query)
            return JsonResponse(video_data_list, safe=False)
        except Exception as e:
            print(f"Error in search view: {e}")
            return JsonResponse({'error': 'Failed to search videos'}, status=500)

def progress_hook(d):
    if d['status'] == 'finished':
        print(f"Done downloading {d['filename']}")

@csrf_exempt
def download(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        video_url = data.get('url')

        if not video_url:
            return JsonResponse({'error': 'URL parameter is missing'}, status=400)

        temp_dir = "temp"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        def sanitize_filename(filename):
            return re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', filename)

        def download_and_convert_video(url):
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                'noplaylist': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'progress_hooks': [progress_hook], 
            }

            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                    downloaded_files = [f for f in os.listdir(temp_dir) if f.endswith('.mp3')]

                    if downloaded_files:
                        temp_audio_path = os.path.join(temp_dir, downloaded_files[0])
                        video_title = sanitize_filename(downloaded_files[0].replace('.mp3', ''))
                        output_audio_path = os.path.join(temp_dir, f'{video_title}.mp3')

                        if os.path.exists(temp_audio_path):
                            os.rename(temp_audio_path, output_audio_path)
                            print(f"Downloaded audio saved as MP3: {output_audio_path}")
                            return output_audio_path
                    else:
                        print("No MP3 file found in the temp directory.")
                        return None

            except Exception as e:
                print(f"Error: {str(e)}")
                return None

        def cleanup(file_path):
            time.sleep(5)
            if os.path.exists(file_path):
                os.remove(file_path)
            for f in os.listdir(temp_dir):
                if f.endswith('.mp3'):
                    os.remove(os.path.join(temp_dir, f))
            print(f"Temp folder cleared: {temp_dir}")

        file_path = download_and_convert_video(video_url)
        if file_path and os.path.exists(file_path):
            response = FileResponse(
                open(file_path, 'rb'),
                content_type='audio/mpeg',
                headers={'Content-Disposition': f'attachment; filename="{os.path.basename(file_path)}"'}
            )

            
            threading.Thread(target=lambda: cleanup(file_path)).start()
            return response

        return JsonResponse({'error': 'Failed to download video'}, status=500)
