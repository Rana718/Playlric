from django.http import JsonResponse, FileResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import threading
import gridfs
from bson.objectid import ObjectId
from .data.utils import download_and_convert_video, get_video_data, cleanup
from .data.music_info import all_details
from .data.tasks import fetch_next_video_data
from .mongo import get_mongo_clinet
import os

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

@csrf_exempt
def download(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        video_url = data.get('url')
        video_title = data.get('title')

        db = get_mongo_clinet()
        collection = db['song_list']
        document = collection.find_one({'title': video_title})

        if document:
            file_id = document.get('song')
            fs = gridfs.GridFS(db)
            song_file = fs.get(ObjectId(file_id))
            response = HttpResponse(song_file.read(), content_type='audio/mpeg')
            response['Content-Disposition'] = f'attachment; filename="{song_file.filename}"'

            
            threading.Thread(target=lambda: fetch_next_video_data(video_url)).start()

            return response

        if not video_url:
            return JsonResponse({'error': 'URL parameter is missing'}, status=400)

        video_data = get_video_data(video_url)
        if not video_data:
            return JsonResponse({'error': 'Failed to extract video data'}, status=500)

        video_url = video_data['url']
        video_title = video_data['title']
        thumbnail_url = video_data['thumbnail_url']

        temp_dir = "temp"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        file_path = download_and_convert_video(video_url, temp_dir)
        if file_path and os.path.exists(file_path):
            response = FileResponse(
                open(file_path, 'rb'),
                content_type='audio/mpeg',
                headers={'Content-Disposition': f'attachment; filename="{os.path.basename(file_path)}"'}
            )

            
            threading.Thread(target=lambda: cleanup(file_path, video_title, thumbnail_url, db, temp_dir)).start()
            threading.Thread(target=lambda: fetch_next_video_data(video_url)).start()

            return response

        return JsonResponse({'error': 'Failed to download video'}, status=500)
