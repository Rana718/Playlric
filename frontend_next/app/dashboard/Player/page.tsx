"use client";
import React, { useEffect } from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '@/redux/store';
import { FaPlay, FaPause } from 'react-icons/fa';
import { Button } from '@/components/ui/button';
import { useRouter } from 'next/navigation';

interface PlayerProps {
    isPlaying: boolean;
    togglePlayPause: () => void;
    audioRef: React.RefObject<HTMLAudioElement>;
}

const Player: React.FC<PlayerProps> = ({ isPlaying, togglePlayPause, audioRef }) => {
    const { url, title, thumbnail_url } = useSelector((state: RootState) => state.video);
    const router = useRouter();

    if (!url) {
        return <div className="text-center text-red-500">No song selected to play.</div>;
    }

    return (
        <div className="flex flex-col items-center p-4">
            <Button onClick={() => router.back()} />
            <h1 className="text-xl font-semibold mb-4">{title}</h1>
            <img src={thumbnail_url} alt={title} className="w-96 h-56 object-cover mb-4" />
            <audio ref={audioRef} src={url} className="w-full max-w-lg" />
            <button
                onClick={togglePlayPause}
                className="mt-4 px-6 py-2 bg-blue-500 text-white rounded-full flex items-center justify-center"
            >
                {isPlaying ? <FaPause className="mr-2" /> : <FaPlay className="mr-2" />}
                {isPlaying ? 'Pause' : 'Play'}
            </button>
        </div>
    );
};

export default Player;
