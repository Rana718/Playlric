import React from 'react';

function Content({ songs, onSongSelect, isLoading }) {
  return (
    <div className="flex-1 p-4 max-h-full overflow-y-auto hide-scrollbar">
      {isLoading ? (
        <div className="flex justify-center items-center h-full">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-white"></div>
        </div>
      ) : (
        <>
          <h2 className="text-2xl font-bold mb-4">Search Results</h2>
          <div className="space-y-4">
            {songs.map((song, index) => (
              <div key={song.id || index}
                className="bg-gray-700 p-4 rounded cursor-pointer flex items-center transition-transform duration-300 ease-in-out transform hover:scale-80"
                onClick={() => onSongSelect(song)}>
                  
                <img src={song.image_url} alt={song.title} className="w-22 h-16 rounded mr-4" />
                <div className="flex flex-col overflow-hidden">
                  <h3 className="text-lg font-semibold text-white truncate">{song.title}</h3>
                  <p className="text-sm text-gray-400">{song.duration}</p>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}

export default Content;
