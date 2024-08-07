import React, { useState } from "react";

function Navbar({ onSearch }){
    const [query, setQuery] = useState('');

    const handleSearch = (e) =>{
        e.preventDefault();
        onSearch(query);
    };

    return(
        <div className="h-16 bg-gray-800 flex items-center px-4">
            <h1 className="text-xl font-bold">Music Player</h1>
            <form onSubmit={handleSearch} className="ml-auto flex items-center">
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}  // Corrected here
                    placeholder="Search..."
                    className="bg-gray-700 text-white px-3 py-1 rounded-l"
                />
                <button type="submit" className="bg-blue-600 px-3 py-1 rounded-r">
                    Search
                </button>
            </form>
        </div>
    );
};

export default Navbar;