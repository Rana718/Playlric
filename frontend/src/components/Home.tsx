import React from 'react';
import { useAppDispatch, useAppSelector } from '@/redux/hooks';
import { downloadSong, fetchNextVideo } from '@/redux/features/searchSlice';
import { useNavigate } from 'react-router-dom';

const Home: React.FC = () => {
    const { songs, status, error } = useAppSelector((state) => state.search);
    const dispatch = useAppDispatch();
    const navigate = useNavigate();

    if (status === 'loading') {
        return (
            <div className="flex justify-center items-center min-h-screen">
                <span className="text-lg font-semibold">Loading...</span>
            </div>
        );
    }

    if (status === 'failed') {
        return (
            <div className="flex justify-center items-center min-h-screen">
                <span className="text-lg font-semibold text-red-600">Error: {error}</span>
            </div>
        );
    }

    const handleSongClick = async (song: any) => {
        try {
            // Dispatch the download and fetch the next video
            await dispatch(downloadSong(song)).unwrap();
            const nextSongs = await dispatch(fetchNextVideo(song.songUrl)).unwrap();
            
            // Navigate to the player with current and next songs
            navigate('/player', { state: { currentSong: song, nextSong: nextSongs } });
        } catch (error) {
            console.error("Failed to handle song click:", error);
        }
    };

    return (
        <div>
            {songs.length > 0 ? (
                <div className='space-y-4'>
                    {songs.map((song, index) => (
                        <div key={index}
                            className="bg-gray-700 p-4 rounded cursor-pointer flex items-center transition-transform duration-300 ease-in-out transform hover:scale-80"
                            onClick={() => handleSongClick(song)}
                        >
                            <img src={song.thumbnailUrl} alt={song.title} className="w-22 h-16 rounded mr-4" />
                            <div className="flex flex-col overflow-hidden">
                                <h3 className="text-lg font-semibold text-white truncate">{song.title}</h3>
                            </div>
                        </div>
                    ))}
                </div>
            ) : (
                <div className="text-center text-gray-500">No results found</div>
            )}
        </div>
    );
};

export default Home;
