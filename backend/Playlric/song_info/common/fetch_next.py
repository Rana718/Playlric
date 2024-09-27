from .view_utils import fetch_next_song, JsonResponse


def fetch_next_song_info(url):
    if not url:
        return JsonResponse({'error': 'URL parameter is missing'}, status=400)

    try:
        next_video_info = fetch_next_song(url)
        print(next_video_info)
        return JsonResponse({'next_video': next_video_info})
    except Exception as e:
        print(f"Error fetching next video info: {e}")
        return JsonResponse({'error': 'Failed to fetch next video info'}, status=500)