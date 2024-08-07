from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Video
import json
import os
import yt_dlp as youtube_dl
from .music_info import search_youtube, get_video_details
import re
import threading
import time

@csrf_exempt
def search(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        query = data.get('query')

        video = Video.objects.filter(title__icontains=query).first()
        if video and os.path.exists(video.file_path):
            return StreamingHttpResponse(
                open(video.file_path, 'rb'),
                content_type='audio/mpeg',
                headers={'Content-Disposition': f'attachment; filename="{os.path.basename(video.file_path)}"'}
            )

        video_data_list = search_youtube(query, max_results=10)
        get_video_details(video_data_list)

        return JsonResponse(video_data_list, safe=False)

@csrf_exempt
def download(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        video_url = data.get('url')
        title = data.get('title')

        video = Video.objects.filter(title=title).first()
        if video:
            if os.path.exists(video.file_path):
                response = StreamingHttpResponse(
                    open(video.file_path, 'rb'),
                    content_type='audio/mpeg',
                    headers={'Content-Disposition': f'attachment; filename="{os.path.basename(video.file_path)}"'}
                )
                def cleanup():
                    time.sleep(5)  # Wait for 5 seconds
                    if os.path.exists(video.file_path):
                        os.remove(video.file_path)
                # Schedule cleanup after response is sent
                threading.Thread(target=cleanup).start()
                return response
            else:
                video.delete()

        temp_dir = "temp"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        def sanitize_filename(filename):
            return re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', filename)

        def get_video_info(url):
            ydl_opts = {
                'format': 'bestaudio/best'
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                try:
                    info_dict = ydl.extract_info(url, download=False)
                    return info_dict
                except Exception as e:
                    print(f"Error: {str(e)}")
                    return None

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
            }

            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info_dict = get_video_info(url)
                    if not info_dict:
                        print("Failed to retrieve video information.")
                        return None

                    video_title = info_dict.get('title', 'audio').replace("/", "-")
                    video_title = sanitize_filename(video_title)
                    output_audio_path = os.path.join(temp_dir, f'{video_title}.mp3')

                    ydl.download([url])

                    downloaded_files = [f for f in os.listdir(temp_dir) if f.endswith('.mp3')]
                    if downloaded_files:
                        temp_audio_path = os.path.join(temp_dir, downloaded_files[0])
                        os.rename(temp_audio_path, output_audio_path)
                        print(f"Downloaded audio saved as MP3: {output_audio_path}")
                        return output_audio_path
                    else:
                        print("No MP3 file found in the temp directory.")
                        return None

            except Exception as e:
                print(f"Error: {str(e)}")
                return None

        file_path = download_and_convert_video(video_url)
        if file_path and os.path.exists(file_path):
            Video.objects.create(title=title, url=video_url, thumbnail_url="", file_path=file_path)
            response = StreamingHttpResponse(
                open(file_path, 'rb'),
                content_type='audio/mpeg',
                headers={'Content-Disposition': f'attachment; filename="{os.path.basename(file_path)}"'}
            )

            def cleanup():
                time.sleep(5)
                if os.path.exists(file_path):
                    os.remove(file_path)

            
            threading.Thread(target=cleanup).start()
            return response

        return JsonResponse({'error': 'Failed to download video'}, status=500)
