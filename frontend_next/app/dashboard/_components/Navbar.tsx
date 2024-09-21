"use client";
import React, { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { useAppDispatch } from '@/hooks/hooks';
import { fetchSearchResults } from '@/redux/slices/searchSlice';

const Navbar: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const dispatch = useAppDispatch();

  const handleSearch = () => {
    dispatch(fetchSearchResults(searchTerm)); 
  };

  return (
    <div className="flex items-center justify-between px-4 py-2 bg-gray-800">
      <Input
        type="text"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        placeholder="Search videos..."
        className="w-full max-w-xs px-4 py-2 text-white"
      />
      <Button
        onClick={handleSearch}
        className="ml-4 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        Search
      </Button>
    </div>
  );
};

export default Navbar;
