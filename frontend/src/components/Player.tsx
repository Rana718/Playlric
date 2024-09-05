import React, { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

interface Song {
    title: string;
    url: string;
    thumbnailUrl: string;
    duration: string;
}

export default function Player() {
    const location = useLocation();
    const { currentSong, nextSong } = location.state as { currentSong: Song; nextSong: Song[] };

    // Log to check if data is passed correctly
    useEffect(() => {
        console.log('Current Song:', currentSong);
        console.log('Next Songs:', nextSong);
    }, [currentSong, nextSong]);

    if (!currentSong) {
        return <div className="text-center text-gray-500">No song is currently playing</div>;
    }

    return (
        <div className='p-4'>
            <h1 className='text-2xl font-bold mb-4'>Now Playing</h1>
            <div className='bg-gray-800 p-4 rounded'>
                {/* Check if thumbnailUrl exists */}
                <img src={currentSong.thumbnailUrl || '/placeholder-image.png'} alt={currentSong.title} className='w-32 h-32 rounded mb-4' />
                <h2 className='text-xl font-semibold text-white mb-2'>{currentSong.title}</h2>
                {/* Check if URL exists */}
                <audio controls className='w-full'>
                    <source src={currentSong.url} type="audio/mpeg" />
                    Your browser does not support the audio element.
                </audio>
            </div>

            {nextSong.length > 0 && (
                <div className='mt-4 p-4 bg-gray-700 rounded'>
                    <h2 className='text-xl font-bold text-white'>Next Songs</h2>
                    {nextSong.map((song, index) => (
                        <div key={index} className='flex items-center mb-4'>
                            <img src={song.thumbnailUrl || '/placeholder-image.png'} alt={song.title} className='w-16 h-16 rounded mr-4' />
                            <div className='flex flex-col'>
                                <p className='text-white'>{song.title}</p>
                                <p className='text-gray-400'>{song.duration}</p>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
