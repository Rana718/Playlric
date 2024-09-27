import os
import re
import yt_dlp as youtube_dl
import gridfs
from bson.objectid import ObjectId
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

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

def get_video_data(video_url):
    try:
        
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--remote-debugging-port=9222')

        # Initialize WebDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        # Fetch the video page
        driver.get(video_url)
        time.sleep(5)  # Let the page load

        # Find related video elements (limit to 20)
        related_videos = []
        video_elements = driver.find_elements(By.XPATH, '//a[@href and contains(@href, "/watch?v=")]')

        # Extract video IDs and ensure not to include the current video
        current_video_id = video_url.split('watch?v=')[-1]
        for elem in video_elements:
            video_url_get = elem.get_attribute('href')
            video_id = video_url_get.split('watch?v=')[-1].split('&')[0]

            # Avoid duplicates and the current video
            if video_id != current_video_id and video_url_get not in related_videos:
                related_videos.append(video_url_get)
            
            # Stop when we have 20 videos
            if len(related_videos) >= 20:
                break

        driver.quit()
        return related_videos

    except Exception as e:
        print(f"Error fetching related videos: {e}")
        return []