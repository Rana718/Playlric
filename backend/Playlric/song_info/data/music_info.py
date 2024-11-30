import requests
from bs4 import BeautifulSoup
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
import yt_dlp

def get_youtube_urls(query, num_urls=30):
    urls = []
    search_url_template = "https://www.google.com/search?q=site:youtube.com+{query}&start={start}"
    headers = {"User-Agent": "Mozilla/5.0"}
    for start in range(0, num_urls, 10):
        search_url = search_url_template.format(query=urllib.parse.quote(query), start=start)
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

def get_youtube_video_info_ytdlp(video_url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'force_generic_extractor': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return {
                'title': info.get('title', 'No title found'),
                'thumbnail': info.get('thumbnail', 'No image URL found'),
                'duration': info.get('duration', 0)
            }
    except Exception as e:
        print(f"Error retrieving video info for {video_url}: {e}")
        return {
            'title': 'No title found',
            'thumbnail': 'No image URL found',
            'duration': 0
        }

def fetch_video_details_batch(video_urls):
    results = []
    with ThreadPoolExecutor(max_workers=min(10, len(video_urls))) as executor:
        future_to_url = {executor.submit(get_youtube_video_info_ytdlp, url): url for url in video_urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                video_info = future.result()
                result = {
                    'url': url,
                    'title': video_info['title'],
                    'image_url': video_info['thumbnail'],
                    'duration': format_duration(video_info['duration'])
                }
                results.append(result)
            except Exception as exc:
                print(f"Error processing {url}: {exc}")
    return results

def process_video_data(input_data):
    if isinstance(input_data, dict):
        if 'next_video' in input_data:
            video_urls = input_data['next_video'][0]['url']
        elif 'url' in input_data:
            video_urls = [input_data['url']]
        else:
            video_urls = []
    elif isinstance(input_data, str):
        video_urls = [input_data]
    elif isinstance(input_data, list):
        video_urls = input_data
    else:
        print("Unsupported input format")
        return []
    return fetch_video_details_batch(video_urls)

def all_details(query, is_url=False):
    if is_url:
        print(query)
        return process_video_data(query)
    else:
        video_urls = get_youtube_urls(query)
        return fetch_video_details_batch(video_urls)
