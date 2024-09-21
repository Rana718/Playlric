"use client";
import React, { useEffect, useRef } from 'react';
import Navbar from './_components/Navbar';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '@/redux/store';
import FooterPlayer from './_components/FooterPlayer';
import { setIsPlaying, setCurrentTime } from '@/redux/slices/audioSlice';

function DashboardLayout({ children }: { children: React.ReactNode }) {
  const dispatch = useDispatch();
  const { fileUrl, isPlaying, currentTime } = useSelector((state: RootState) => state.audio); // Access global audio state
  const audioRef = useRef<HTMLAudioElement | null>(null);

  // Toggle play and pause
  const togglePlayPause = () => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
        dispatch(setIsPlaying(false));
      } else {
        audioRef.current.play();
        dispatch(setIsPlaying(true));
      }
    }
  };

  // Update current time in the global state as the audio plays
  const handleTimeUpdate = () => {
    if (audioRef.current) {
      dispatch(setCurrentTime(audioRef.current.currentTime));
    }
  };

  // Sync play/pause state with the audio element only if there's an actual change
  useEffect(() => {
    if (audioRef.current) {
      if (isPlaying && audioRef.current.paused) {
        audioRef.current.play();
      } else if (!isPlaying && !audioRef.current.paused) {
        audioRef.current.pause();
      }
    }
  }, [isPlaying]);

  // Set the audio element's current time and file source when fileUrl changes
  useEffect(() => {
    if (audioRef.current && fileUrl) {
      audioRef.current.src = fileUrl;
      audioRef.current.load(); // Reload the audio when the source changes
      audioRef.current.currentTime = currentTime; // Sync to the correct current time
    }
  }, [fileUrl]);

  return (
    <div>
      <Navbar />
      <div>{children}</div>
      <FooterPlayer togglePlayPause={togglePlayPause} />
      <audio
        ref={audioRef}
        onTimeUpdate={handleTimeUpdate} // Update time in Redux as the audio progresses
        onLoadedMetadata={() => dispatch(setCurrentTime(0))} // Reset time when new audio loads
      />
    </div>
  );
}

export default DashboardLayout;
