import React, { useState } from 'react';
import { FaBars } from 'react-icons/fa';

function Navbar({ onSearch, toggleSidebar }) {
    const [query, setQuery] = useState('');

    const handleSearch = (e) => {
        e.preventDefault();
        onSearch(query);
    };

    return (
        <div className="h-16 bg-gray-800 flex items-center px-4 shadow-lg relative z-20">
            <button onClick={toggleSidebar} className="text-white text-2xl mr-4">
                <FaBars />
            </button>

            <div className="flex items-center absolute left-1/2 transform -translate-x-1/2">
                <img src="playlyric_logo.png" alt="logo" className='h-12 w-16 mr-2' />
                <h1 className="text-3xl font-bold text-transparent">
                    <span className="animate-rainbow-letter" style={{ '--i': 1 }}>P</span>
                    <span className="animate-rainbow-letter" style={{ '--i': 2 }}>L</span>
                    <span className="animate-rainbow-letter" style={{ '--i': 3 }}>A</span>
                    <span className="animate-rainbow-letter" style={{ '--i': 4 }}>Y</span>
                    <span className="animate-rainbow-letter" style={{ '--i': 5 }}> </span>
                    <span className="animate-rainbow-letter" style={{ '--i': 6 }}>L</span>
                    <span className="animate-rainbow-letter" style={{ '--i': 7 }}>Y</span>
                    <span className="animate-rainbow-letter" style={{ '--i': 8 }}>R</span>
                    <span className="animate-rainbow-letter" style={{ '--i': 9 }}>I</span>
                    <span className="animate-rainbow-letter" style={{ '--i': 10 }}>C</span>
                </h1>
            </div>

            <form onSubmit={handleSearch} className="ml-auto flex items-center space-x-2">
                <div className="flex items-center bg-gray-700 text-white rounded-lg focus-within:ring-2 focus-within:ring-blue-500">
                    <input type="text" value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search..."
                        className="bg-gray-700 text-white px-3 py-2 rounded-l-lg focus:outline-none" />

                    <button type="submit" className="flex items-center justify-center p-1 bg-transparent">
                        <img src="search_icon.gif" alt="Search" className="h-8 w-8" />
                    </button>
                </div>
            </form>
        </div>
    );
}

export default Navbar;
