from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
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

        video_data_list = search_youtube(query, max_results=10)
        get_video_details(video_data_list)
        print(video_data_list)

        return JsonResponse(video_data_list, safe=False)

@csrf_exempt
def download(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        video_url = data.get('url')
        title = data.get('title')

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

                        # Rename the file safely
                        try:
                            os.rename(temp_audio_path, output_audio_path)
                        except FileNotFoundError:
                            print(f"Error: The file {temp_audio_path} was not found.")
                            return None
                        except Exception as e:
                            print(f"Error renaming file: {str(e)}")
                            return None

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
            response = StreamingHttpResponse(
                open(file_path, 'rb'),
                content_type='audio/mpeg',
                headers={'Content-Disposition': f'attachment; filename="{os.path.basename(file_path)}"'}
            )

            def cleanup():
                time.sleep(3)
                # Delete the file after 3 seconds
                if os.path.exists(file_path):
                    os.remove(file_path)
                # Clear the temp folder
                for f in os.listdir(temp_dir):
                    if f.endswith('.mp3'):
                        os.remove(os.path.join(temp_dir, f))
                print(f"Temp folder cleared: {temp_dir}")

            threading.Thread(target=cleanup).start()
            return response

        return JsonResponse({'error': 'Failed to download video'}, status=500)
