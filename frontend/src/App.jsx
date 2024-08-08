import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import Player from './components/Player';
import Content from './components/Content';

function App() {
  const [songs, setSongs] = useState([]);
  const [currentSong, setCurrentSong] = useState(null);
  const [isLoading, setLoading] = useState(false);

  const handleSearch = async (query) =>{
    setLoading(true);
    try{
      const response = await fetch('http://localhost:8000/videos/search/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });
      
      if(!response.ok){
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setSongs(data.slice(0,15));
    }catch(error){
      console.error('There has been a problem with your fetch operation:', error);
    }finally{
      setLoading(false);
    }
  }

  const handleSongSelect = async (song) =>{
    try{
      const response = await fetch('http://localhost:8000/videos/download/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: song.url, title: song.title, thumbnail_url: song.image_url }),
      });

      if(!response.ok){
        throw new Error('Network response was not ok');
      }

      const file = await response.blob();
      const url = URL.createObjectURL(file);

      setCurrentSong({ ...song, audio: url });
    }catch(error){
      console.error('There has been a problem with your fetch operation:', error);
    }
  }

  return (
    <div className="flex h-screen bg-gray-900 text-white">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Navbar onSearch={handleSearch} />
        <Content songs={songs} onSongSelect={handleSongSelect} isLoading={isLoading} />
        <Player currentSong={currentSong} />
      </div>
    </div>
  );
}

export default App;