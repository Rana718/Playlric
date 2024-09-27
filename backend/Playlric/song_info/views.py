from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .common import get_mp3, search, fetch_next_song_info
from django.views import View
import os
import yt_dlp as youtube_dl
from django.utils.decorators import method_decorator



@csrf_exempt
def search_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        query = data.get('query')
        return search(query)
    
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


@csrf_exempt
def download(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        video_url = data.get('url')
        video_title = data.get('title')
        thumbnail_url = data.get('thumbnail_url')
        return get_mp3(video_url, video_title, thumbnail_url)
    
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


@csrf_exempt
def fetch_next_video_info(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        video_url = data.get('url')
        print("Video URL from request:", video_url) 

        return fetch_next_song_info(video_url)
    
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

@method_decorator(csrf_exempt, name='dispatch')
class DownloadVideoView(View):
    
    def post(self, request):
        data = json.loads(request.body)
        url = data.get('url')
        if not url:
            return JsonResponse({'error': 'URL parameter is missing'}, status=400)

        seen_formats = set()

        def list_formats(formats):
            available_formats = []
            for fmt in formats:
                resolution = fmt.get('format_note')
                extension = fmt.get('ext')

                if resolution in ['storyboard', 'Default', 'low', 'medium']:
                    continue

                format_tuple = (resolution, extension)
                if format_tuple in seen_formats:
                    continue

                seen_formats.add(format_tuple)
                if resolution and extension:
                    available_formats.append({
                        'resolution': resolution,
                        'extension': extension,
                        'format_id': fmt['format_id']
                    })

            return available_formats

        ydl_opts = {
            'noplaylist': True,
            'quiet': True,
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                formats = info_dict.get('formats', [])

                available_formats = list_formats(formats)

                if not available_formats:
                    return JsonResponse({'error': 'No available video formats found.'}, status=404)

                return JsonResponse({'available_formats': available_formats}, status=200)
        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    
    def download_video(self, request):
        if request.method == 'POST':
            data = request.POST
            format_id = data.get('format_id')
            url = data.get('url')

            if not format_id or not url:
                return JsonResponse({'error': 'Format ID or URL is missing'}, status=400)

            ydl_opts = {
                'format': format_id,
                'outtmpl': '%(title)s.%(ext)s',
                'noplaylist': True,
            }

            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                    downloaded_files = [f for f in os.listdir('.') if f.endswith('.mp4')]

                    if downloaded_files:
                        video_path = os.path.join(os.getcwd(), downloaded_files[0])
                        return JsonResponse({'video_path': video_path}, status=200)
                    else:
                        return JsonResponse({'error': 'No MP4 file found in the current directory.'}, status=404)
            except Exception as e:
                print(f"Error: {str(e)}")
                return JsonResponse({'error': str(e)}, status=500)
