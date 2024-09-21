// FooterPlayer.tsx
"use client";
import React from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '@/redux/store';

const FooterPlayer: React.FC<{ togglePlayPause: () => void }> = ({ togglePlayPause }) => {
  const { isPlaying, fileUrl } = useSelector((state: RootState) => state.audio);

  return (
    <div className="footer-player">
      <div>{fileUrl ? `Playing: ${fileUrl}` : "No song selected"}</div>
      <button onClick={togglePlayPause}>
        {isPlaying ? 'Pause' : 'Play'}
      </button>
    </div>
  );
};

export default FooterPlayer;
