"use client";
import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '@/redux/store';
import { useRouter } from 'next/navigation';
import { setVideoDetails } from '@/redux/slices/videoSlice';
import { setFileUrl, setIsPlaying, setCurrentTime } from '@/redux/slices/audioSlice';

const SearchResults: React.FC = () => {
    const { results, status } = useSelector((state: RootState) => state.search);
    const dispatch = useDispatch();
    const router = useRouter();

    const handleVideoClick = async (video: { url: string, title: string, image_url: string }) => {
        try {
            const response = await fetch('http://localhost:8000/videos/download/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    url: video.url,
                    title: video.title,
                    thumbnail_url: video.image_url
                }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const file = await response.blob();
            const fileUrl = URL.createObjectURL(file);
            
            dispatch(setFileUrl(fileUrl));
            dispatch(setIsPlaying(true));
            dispatch(setCurrentTime(0));
            dispatch(setVideoDetails({
                url: fileUrl,
                title: video.title,
                thumbnail_url: video.image_url,
            }));

            router.push('/dashboard/Player');
        } catch (error) {
            console.error('Failed to fetch video data:', error);
        }
    };

    if (status === 'loading') {
        return <div className="text-center text-gray-500">Loading...</div>;
    }

    if (status === 'failed') {
        return <div className="text-center text-red-500">Failed to fetch search results.</div>;
    }

    return (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 p-4">
            {results.length > 0 ? (
                results.map((video, index) => (
                    <div
                        key={index}
                        className="video-item bg-white rounded-lg shadow-md overflow-hidden border border-gray-200 cursor-pointer"
                        onClick={() => handleVideoClick(video)}
                    >
                        <img
                            src={video.image_url || '/fallback-image.jpg'}
                            alt={video.title}
                            className="w-full h-48 object-cover"
                        />
                        <div className="p-4">
                            <a className="block text-blue-600 hover:underline font-semibold text-lg">
                                {video.title}
                            </a>
                            <p className="text-sm text-gray-600">Duration: {video.duration}</p>
                        </div>
                    </div>
                ))
            ) : (
                <div className="text-center text-gray-500 col-span-full">No results found.</div>
            )}
        </div>
    );
};

export default SearchResults;
