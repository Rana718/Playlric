from .view_utils import JsonResponse, FileResponse, get_mongo_clinet, gridfs, ObjectId, download_video_convert, os, cleanup_files, threading 


def get_mp3(url, title, image):
    if not url or not title:
        return JsonResponse({'error': 'URL or title parameter is missing'}, status=400)

    db = get_mongo_clinet()
    collection = db['song_list']
    document = collection.find_one({'title': title})
    fs = gridfs.GridFS(db)
    
    if document:
        file_id = document.get('song')
        
        try:
            song_file = fs.get(ObjectId(file_id))
            response = FileResponse(
                song_file,
                content_type='audio/mpeg',
                as_attachment=True,
                filename=f"{title}.mp3"
            )
            return response
        
        except gridfs.NoFile:
            return JsonResponse({'error': 'File not found in GridFS'}, status=404)
    else:
        temp_dir = "temp"
        os.makedirs(temp_dir, exist_ok=True)
        file_path = download_video_convert(url, temp_dir)
        if file_path and os.path.exists(file_path):
            try:
               
                def handle_file_cleanup():
                    try:
                        with open(file_path, 'rb') as f:
                            file_id = fs.put(f, filename=f"{title}.mp3")
                        collection.insert_one({'title': title, 'song': file_id})
                    finally:
                        cleanup_files(file_path, title, image, db, temp_dir)
                response = FileResponse(
                    open(file_path, 'rb'),
                    content_type='audio/mpeg',
                    as_attachment=True,
                    filename=f"{title}.mp3"
                )
                
                threading.Thread(target=handle_file_cleanup).start()
                return response
            except Exception as e:
                print(f"Error sending file: {str(e)}")
                return JsonResponse({'error': 'Failed to process video'}, status=500)
        else:
            return JsonResponse({'error': 'Failed to download video'}, status=500)