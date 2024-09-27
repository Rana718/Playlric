from .view_utils import video_details, JsonResponse

def search(query):
    if not query:
        return JsonResponse({'error': 'Query parameter is missing'}, status=400)

    try:
        video_data_list = video_details(query)
            
        return JsonResponse(video_data_list, safe=False)
    except Exception as e:
        return JsonResponse({'error': e}, status=500)