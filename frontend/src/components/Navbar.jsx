import React, { useState } from "react";

function Navbar({ onSearch }){
    const [query, setQuery] = useState('');

    const handleSearch = (e) =>{
        e.preventDefault();
        onSearch(query);
    };

    return(
        <div className="h-16 bg-gray-800 flex items-center px-4 shadow-lg">
            <h1 className="text-xl font-bold text-white">Music Player</h1>
            <form onSubmit={handleSearch} className="ml-auto flex items-center space-x-2">
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Search..."
                    className="bg-gray-700 text-white px-3 py-1 rounded-l focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded-r hover:bg-blue-500 transition duration-300 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500">
                    Search
                </button>
            </form>
        </div>
    );
};

export default Navbar;