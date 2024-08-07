from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from threading import Thread
import requests
from bs4 import BeautifulSoup
import time
from .user_agents import get_random_user_agent

def search_youtube(query, max_results=10):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    user_agent = get_random_user_agent()
    options.add_argument(f'user-agent={user_agent}')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    driver.get(url)
    
    time.sleep(2)
    
    video_elements = driver.find_elements(By.CSS_SELECTOR, 'a#video-title')[:max_results]
    
    video_data = [{'url': element.get_attribute('href')} for element in video_elements]
    
    driver.quit()
    return video_data

def get_youtube_video_info(video_url):
    headers = {"User-Agent": get_random_user_agent()}
    
    response = requests.get(video_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    title_tag = soup.find("meta", property="og:title")
    title = title_tag["content"] if title_tag else "Title not found"
    
    thumbnail_tag = soup.find("meta", property="og:image")
    thumbnail_url = thumbnail_tag["content"] if thumbnail_tag else "Thumbnail not found"
    
    return title, thumbnail_url

def fetch_video_details(video_data):
    try:
        title, thumbnail_url = get_youtube_video_info(video_data['url'])
        video_data['title'] = title
        video_data['image_url'] = thumbnail_url
    except Exception as e:
        video_data['title'] = "No title found"
        video_data['image_url'] = "No image URL found"

def get_video_details(video_data_list):
    threads = []

    for video_data in video_data_list:
        thread = Thread(target=fetch_video_details, args=(video_data,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
