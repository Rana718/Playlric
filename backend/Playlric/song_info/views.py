from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Video
import json
import os
import yt_dlp as youtube_dl
from .music_info import search_youtube, get_video_details

@csrf_exempt
def search(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        query = data.get('query')

        # Check if the song is already in the database
        video = Video.objects.filter(title__icontains=query).first()
        if video and os.path.exists(video.file_path):
            return FileResponse(open(video.file_path, 'rb'), as_attachment=True, filename=os.path.basename(video.file_path))

        # If not in the database, search and download
        video_data_list = search_youtube(query, max_results=10)
        get_video_details(video_data_list)

        return JsonResponse(video_data_list, safe=False)

@csrf_exempt
def download(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        video_url = data.get('url')
        title = data.get('title')

        # Check if the song is already in the database
        video = Video.objects.filter(title=title).first()
        if video:
            if os.path.exists(video.file_path):
                return FileResponse(open(video.file_path, 'rb'), as_attachment=True, filename=os.path.basename(video.file_path))
            else:
                video.delete()

        temp_dir = "temp"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

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
                'format': 'worstvideo[height<=144]+bestaudio/best',
                'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                'noplaylist': True,
                'merge_output_format': 'mp4'
            }

            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info_dict = get_video_info(url)
                    if not info_dict:
                        print("Failed to retrieve video information.")
                        return None

                    video_title = info_dict.get('title', 'video').replace("/", "-")
                    output_video_path = os.path.join(temp_dir, f'{video_title}.mp4')

                    ydl.download([url])

                    downloaded_files = [f for f in os.listdir(temp_dir) if f.endswith('.mp4')]
                    if downloaded_files:
                        temp_video_path = os.path.join(temp_dir, downloaded_files[0])
                        os.rename(temp_video_path, output_video_path)
                        print(f"Downloaded video saved as MP4: {output_video_path}")
                        return output_video_path
                    else:
                        print("No MP4 file found in the temp directory.")
                        return None

            except Exception as e:
                print(f"Error: {str(e)}")
                return None
            finally:
                # Clean up temp files
                for f in os.listdir(temp_dir):
                    os.remove(os.path.join(temp_dir, f))

        file_path = download_and_convert_video(video_url)
        if file_path:
            Video.objects.create(title=title, url=video_url, thumbnail_url="", file_path=file_path)
            return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))

        return JsonResponse({'error': 'Failed to download video'}, status=500)