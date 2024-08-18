from .utils import get_video_data
def fetch_next_video_data(video_url):
    try:
        next_video_data = get_video_data(video_url)
        print(f"Next video data: {next_video_data}")
    except Exception as e:
        print(f"Error fetching next video data: {e}")