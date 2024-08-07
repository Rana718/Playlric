import React from "react";

function Sidebar(){
    return(
        <div className="w-64 bg-gray-800 p-4">
            <ul>
                <li className="mb-2"><a href="#" className="text-white">Home</a></li>
                <li className="mb-2"><a href="#" className="text-white">Search</a></li>
                <li className="mb-2"><a href="#" className="text-white">Your Library</a></li>
            </ul>
        </div>
    );
};


export default Sidebar;