import React from "react";
import { FaTimes } from 'react-icons/fa';

function Sidebar({ isOpen, toggleSidebar }) {
  return (
    <>
      <div className={`fixed top-0 left-0 h-full w-36 bg-gray-800 p-4 transition-transform duration-300 transform ${isOpen ? 'translate-x-0' : '-translate-x-full'} z-30`}>
        <button onClick={toggleSidebar} className="text-white text-2xl mb-4">
          <FaTimes />
        </button>
        <ul>
          <li className="mb-2">
            <a href="#" className="text-white hover:bg-gray-700 p-2 rounded block">
              Home
            </a>
          </li>
          <li className="mb-2">
            <a href="#" className="text-white hover:bg-gray-700 p-2 rounded block">
              Search
            </a>
          </li>
          <li className="mb-2">
            <a href="#" className="text-white hover:bg-gray-700 p-2 rounded block">
              Your Library
            </a>
          </li>
        </ul>
      </div>
    </>
  );
}

export default Sidebar;
