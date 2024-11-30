import yt_dlp as youtube_dl
import gridfs
from bson.objectid import ObjectId
import os
import re
import yt_dlp as youtube_dl
import time
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', filename)

def download_and_convert_video(url, temp_dir):
    def progress_hook(d):
        if d['status'] == 'finished':
            print(f"Done downloading {d['filename']}")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'cookiefile': 'cookies.txt',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [progress_hook],
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            downloaded_files = [f for f in os.listdir(temp_dir) if f.endswith('.mp3')]

            if downloaded_files:
                temp_audio_path = os.path.join(temp_dir, downloaded_files[0])
                video_title = sanitize_filename(downloaded_files[0].replace('.mp3', ''))
                output_audio_path = os.path.join(temp_dir, f'{video_title}.mp3')
                os.rename(temp_audio_path, output_audio_path)
                print(f"Downloaded audio saved as mp3: {output_audio_path}")
                return output_audio_path
            else:
                print("No MP3 file found in the temp directory.")
                return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
    
def cleanup(file_path, video_title, thumbnail_url, db, temp_dir):
    try:
        fs = gridfs.GridFS(db)
        path = file_path

        with open(path, 'rb') as f:
            file_id = fs.put(f, filename=f"{video_title}.mp3", metadata={'type': 'audio', 'thumbnail_url': thumbnail_url})
        collection = db['song_list']
        document = {
            'title': video_title,
            'song': file_id,
        }
        collection.insert_one(document)

        time.sleep(5)
        if os.path.exists(file_path):
            os.remove(file_path)
        for f in os.listdir(temp_dir):
            if f.endswith('.mp3'):
                os.remove(os.path.join(temp_dir, f))
        print(f"Temp folder cleared: {temp_dir}")
    except Exception as e:
        print(f"Error: {str(e)}")

def get_video_data(video_url: str, max_videos: int = 20, timeout: int = 10) -> List[str]:
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')  # Disable image loading
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        service = Service(ChromeDriverManager().install())
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-browser-side-navigation')
        chrome_options.add_argument('--disable-web-security')
        with webdriver.Chrome(service=service, options=chrome_options) as driver:
            driver.get(video_url)
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, '//a[@href and contains(@href, "/watch?v=")]'))
            )
            
            current_video_id = video_url.split('watch?v=')[-1].split('&')[0]
            related_video_elements = driver.find_elements(By.XPATH, '//a[@href and contains(@href, "/watch?v=")]')
            related_videos = set()
            
            for elem in related_video_elements:
                try:
                    video_url_get = elem.get_attribute('href')
                    
                    if not video_url_get:
                        continue
                    
                    video_id = video_url_get.split('watch?v=')[-1].split('&')[0]
                    
                    if video_id != current_video_id and video_url_get not in related_videos:
                        related_videos.add(video_url_get)
                        
                        if len(related_videos) >= max_videos:
                            break
                
                except Exception as elem_error:
                    print(f"Error processing video element: {elem_error}")
            
            return list(related_videos)
    
    except Exception as e:
        print(f"Comprehensive error in get_video_data: {e}")
        return []

def validate_youtube_url(url: str) -> bool:
    youtube_regex = (
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    return re.match(youtube_regex, url) is not None

def async_get_video_data(video_urls: List[str], max_videos_per_url: int = 20) -> List[str]:
    valid_urls = [url for url in video_urls if validate_youtube_url(url)]
    
    all_related_videos = []
    with ThreadPoolExecutor(max_workers=min(5, len(valid_urls))) as executor:
        future_to_url = {
            executor.submit(get_video_data, url, max_videos_per_url): url 
            for url in valid_urls
        }
        
        for future in as_completed(future_to_url):
            try:
                related_videos = future.result()
                all_related_videos.extend(related_videos)
            except Exception as exc:
                print(f"URL retrieval generated an exception: {exc}")
    
    return list(set(all_related_videos))
