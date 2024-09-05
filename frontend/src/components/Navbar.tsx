import React, { useState } from 'react';
import { useAppDispatch } from '@/redux/hooks';
import { setSearchTerm, fetchSongData } from '@/redux/features/searchSlice';
import { Input } from '../components/ui/input';
import { Button } from '../components/ui/button';

const Navbar: React.FC = () => {
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);
    const [inputValue, setInputValue] = useState('');
    const dispatch = useAppDispatch();

    const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setInputValue(e.target.value);
    };

    const handleSearchSubmit = () => {
        dispatch(setSearchTerm(inputValue));
        dispatch(fetchSongData(inputValue));
    };

    const toggleSidebar = () => {
        setIsSidebarOpen(!isSidebarOpen);
    };

    return (
        <div>
            {/* Navbar */}
            <nav className="bg-blue-600 p-4 flex justify-between items-center">
                <div className="flex items-center space-x-4">
                    <Button className="md:hidden" onClick={toggleSidebar}>
                        {isSidebarOpen ? '✕' : '☰'} {/* Toggle Menu Icon */}
                    </Button>
                    <Input
                        value={inputValue}
                        placeholder="Search..."
                        className="px-3 py-2 rounded-md"
                        onChange={handleSearchChange}
                    />
                    <Button onClick={handleSearchSubmit}>send</Button>
                </div>
            </nav>

            {/* Sidebar */}
            <div
                className={`fixed top-0 left-0 w-64 h-full bg-gray-800 p-4 transition-transform transform ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
                    }`}
            >
                <Button onClick={toggleSidebar} className="text-white">
                    ✕ Close
                </Button>
                <ul className="mt-4">
                    <li className="text-white">Item 1</li>
                    <li className="text-white">Item 2</li>
                </ul>
            </div>
        </div>
    );
};

export default Navbar;
