from .utils import get_video_data
from .music_info import all_details

def fetch_next_video_data(video_url):
    try:
        next_video_urls = get_video_data(video_url)
        next_video_all_data = all_details(next_video_urls, is_url=True)
        return next_video_all_data
        
    except Exception as e:
        print(f"Error fetching next video data: {e}")
        return {'error': str(e)}
