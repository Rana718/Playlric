import requests
from bs4 import BeautifulSoup
import urllib.parse
from threading import Thread
from pytube import YouTube


def get_youtube_urls(query, num_urls=30):
    urls = []
    search_url_template = "https://www.google.com/search?q=site:youtube.com+{query}&start={start}"
    headers = {"User-Agent": "Mozilla/5.0"}

    for start in range(0, num_urls, 10):
        search_url = search_url_template.format(
            query=urllib.parse.quote(query),
            start=start
        )
        try:
            response = requests.get(search_url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                if "youtube.com/watch" in href:
                    url = urllib.parse.unquote(href.split('&')[0].replace('/url?q=', ''))
                    if url not in urls:
                        urls.append(url)
                    if len(urls) >= num_urls:
                        return urls
        except requests.RequestException as e:
            print(f"Error fetching search results: {e}")
    
    return urls

def format_duration(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes}:{seconds:02}"

def get_youtube_video_info_pytube(video_url):
    try:
        yt = YouTube(video_url)
        title = yt.title
        duration = yt.length
        thumbnail_url = yt.thumbnail_url
        return title, thumbnail_url, duration
    except Exception as e:
        print(f"Error retrieving video info for {video_url}: {e}")
        return "No title found", "No image URL found", 0

def fetch_video_details(video_data):
    try:
        title, thumbnail_url, duration = get_youtube_video_info_pytube(video_data['url'])
        video_data['title'] = title
        video_data['image_url'] = thumbnail_url
        video_data['duration'] = duration
        print(f"Fetched details for {video_data['url']}: {title}, {thumbnail_url}, {duration}")
    except Exception as e:
        video_data['title'] = "No title found"
        video_data['image_url'] = "No image URL found"
        video_data['duration'] = 0
        print(f"Error in fetch_video_details for {video_data['url']}: {e}")


def get_video_details(video_data_list):
    threads = []
    
    for video_data in video_data_list:
        thread = Thread(target=fetch_video_details, args=(video_data,))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

def all_details(query, is_url=False):
    video_data_list = []
    
    # Check if the input is a URL or a query
    if is_url:
        if isinstance(query, list):
            for url in query:
                video_data_list.append({"url": url})
        else:
            video_data_list.append({"url": query})
    else:
        # Fetch video URLs based on the search query
        video_urls = get_youtube_urls(query)
        video_data_list = [{"url": url} for url in video_urls]
    
    # Fetch detailed information for each video in video_data_list
    get_video_details(video_data_list)
    
    results = []
    
    # Format results with fallback for missing details
    for video_data in video_data_list:
        results.append({
            'url': video_data.get('url'),
            'title': video_data.get('title', 'No title found'),
            'image_url': video_data.get('image_url', 'No image URL found'),
            'duration': format_duration(video_data.get('duration', 0)) if video_data.get('duration') else '0:00'
        })
    
    return results

