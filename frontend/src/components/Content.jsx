import React from 'react';

function Content({ songs, onSongSelect }) {
  return (
    <div className="flex-1 p-4 overflow-y-auto">
      <h2 className="text-2xl font-bold mb-4">Search Results</h2>
      <div className="grid grid-cols-4 gap-4">
        {songs.map((song, index) => (
          <div key={song.id || index} className="bg-gray-700 p-4 rounded cursor-pointer" onClick={() => onSongSelect(song)}>
            <img src={song.thumbnail_url} alt={song.title} className="w-full rounded mb-2" />
            <h3 className="text-lg font-semibold">{song.title}</h3>
            <p className="text-sm text-gray-400">{song.artist}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Content;
