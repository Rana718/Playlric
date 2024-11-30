from .utils import get_video_data
from .music_info import all_details
import logging

logger = logging.getLogger(__name__)

def fetch_next_video_data(video_url):
    if not video_url:
        logger.error("No video URL provided")
        return {'error': 'Video URL is required'}
        
    try:
        next_video_urls = get_video_data(video_url)
        if not next_video_urls:
            logger.warning(f"No related videos found for {video_url}")
            return {'error': 'No related videos found'}
            
        next_video_all_data = all_details(next_video_urls, is_url=True)
        return next_video_all_data
        
    except Exception as e:
        logger.error(f"Error fetching next video data: {e}", exc_info=True)
        return {'error': str(e)}
