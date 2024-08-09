import React, { useRef, useEffect, useState } from 'react';
import { TfiLoop } from "react-icons/tfi";
import { HiOutlineSwitchHorizontal } from "react-icons/hi";
import { FaPlay, FaPause } from 'react-icons/fa';

function Player({ currentSong, musicload }) {
  const audioRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isLooping, setIsLooping] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);

  useEffect(() => {
    const audio = audioRef.current;

    if (currentSong) {
      audio.src = currentSong.audio;
      audio.play();
      setIsPlaying(true);

      const handleLoadedMetadata = () => {
        setDuration(audio.duration);
      };

      const handleTimeUpdate = () => {
        setCurrentTime(audio.currentTime);
      };

      const handleSongEnd = () => {
        if (isLooping) {
          audio.currentTime = 0;
          audio.play();
        } else {
          setIsPlaying(false);
        }
      };

      audio.addEventListener('loadedmetadata', handleLoadedMetadata);
      audio.addEventListener('timeupdate', handleTimeUpdate);
      audio.addEventListener('ended', handleSongEnd);

      return () => {
        audio.removeEventListener('loadedmetadata', handleLoadedMetadata);
        audio.removeEventListener('timeupdate', handleTimeUpdate);
        audio.removeEventListener('ended', handleSongEnd);
      };
    }
  }, [currentSong, isLooping]);

  const togglePlayPause = () => {
    const audio = audioRef.current;
    if (isPlaying) {
      audio.pause();
    } else {
      audio.play();
    }
    setIsPlaying(!isPlaying);
  };

  const toggleLoop = () => {
    setIsLooping(!isLooping);
  };

  const handleTimeChange = (e) => {
    const newTime = e.target.value;
    audioRef.current.currentTime = newTime;
    setCurrentTime(newTime);
  };

  const formatTime = (time) => {
    if (isNaN(time)) return "0:00";
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
  };

  return (
    <div className="h-24 bg-gray-800 flex flex-col justify-center px-4">
      {currentSong ? (
        <>
          {musicload ? (
            <div className='text-white'>Loading....</div>
          ):(
            <>
              <div className="flex items-center justify-between">
              <div className="flex items-center">
                <img src={currentSong.image_url} alt="Album" className="w-16 h-10 rounded mr-4" />
                <div className="flex flex-col overflow-hidden">
                  <h3 className="text-lg font-semibold text-white truncate">
                    {currentSong.title}
                  </h3>
                  <p className="text-sm text-gray-400">{currentSong.artist}</p>
                </div>
              </div>
              <div className="flex items-center">
                <button onClick={togglePlayPause} className="text-white text-2xl mx-4">
                  {isPlaying ? <FaPause /> : <FaPlay />}
                </button>
                <audio ref={audioRef} className="hidden" />
                <button onClick={toggleLoop} className={`text-white text-2xl ${isLooping ? 'text-blue-500' : ''}`}>
                  {isLooping ? <TfiLoop /> : <HiOutlineSwitchHorizontal />}
                </button>
              </div>
            </div>
            <div className="flex items-center mt-2">
              <span className="text-sm text-gray-400">
                {formatTime(currentTime)}
              </span>
              <input type="range" min="0" max={duration || 0} value={currentTime} onChange={handleTimeChange} className="mx-4 flex-1" />
              <span className="text-sm text-gray-400">
                {formatTime(duration)}
              </span>
            </div>
            </>
          )}
          
        </>
      ) : (
        <p className="text-gray-400">Select a song to play</p>
      )}
    </div>
  );
}

export default Player;
