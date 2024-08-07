import React, { useRef, useEffect } from 'react';

function Player({ currentSong }) {
  const audioRef = useRef(null);

  useEffect(() => {
    if (currentSong && audioRef.current) {
      audioRef.current.play();
    }
  }, [currentSong]);

  return (
    <div className="h-24 bg-gray-800 flex items-center justify-between px-4">
      {currentSong ? (
        <>
          <div className="flex items-center">
            <img src={currentSong.image} alt="Album" className="w-12 h-12 rounded mr-4" />
            <div>
              <h3 className="text-lg font-semibold">{currentSong.title}</h3>
              <p className="text-sm text-gray-400">{currentSong.artist}</p>
            </div>
          </div>
          <audio ref={audioRef} src={currentSong.audio} controls className="flex-1 mx-4" />
        </>
      ) : (
        <p className="text-gray-400">Select a song to play</p>
      )}
    </div>
  );
}

export default Player;
