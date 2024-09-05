import { createAsyncThunk, createSlice, PayloadAction } from '@reduxjs/toolkit';
import axios from 'axios';

const apiUrl = import.meta.env.VITE_API_URL;

interface Song {
    title: string;
    songUrl: string;
    thumbnailUrl: string;
    duration: string;
}

interface SearchState {
    searchTerm: string;
    songs: Song[];
    status: 'idle' | 'loading' | 'succeeded' | 'failed';
    error: string | null;
    currentSong: Song | null;
    nextSong: Song[];
}

const initialState: SearchState = {
    searchTerm: '',
    songs: [],
    status: 'idle',
    error: null,
    currentSong: null,
    nextSong: [],
};

export const fetchSongData = createAsyncThunk(
    'search/fetchSongData',
    async (searchTerm: string) => {
        const response = await axios.post(`${apiUrl}/videos/search/`, { query: searchTerm });
        return response.data;
    }
);

export const downloadSong = createAsyncThunk(
    'search/downloadSong',
    async (song: Song) => {
        const response = await axios.post(`${apiUrl}/videos/download/`, {
            url: song.songUrl,
            title: song.title,
            thumbnail_url: song.thumbnailUrl,
        }, {
            responseType: 'blob',
        });
        return {
            song,
            file: response.data,
        };
    }
);

export const fetchNextVideo = createAsyncThunk(
    'search/fetchNextVideo',
    async (songUrl: string) => {
        const response = await axios.post(`${apiUrl}/videos/next/`, {
            url: songUrl,
        });
        return response.data;
    }
);

const searchSlice = createSlice({
    name: 'search',
    initialState,
    reducers: {
        setSearchTerm: (state, action: PayloadAction<string>) => {
            state.searchTerm = action.payload;
        },
    },
    extraReducers: (builder) => {
        builder
            .addCase(fetchSongData.pending, (state) => {
                state.status = 'loading';
                state.songs = [];
                state.error = null;
            })
            .addCase(fetchSongData.fulfilled, (state, action) => {
                state.status = 'succeeded';
                state.songs = action.payload.map((song: any) => ({
                    title: song.title,
                    songUrl: song.url,
                    thumbnailUrl: song.image_url,
                    duration: song.duration,
                }));
            })
            .addCase(fetchSongData.rejected, (state, action) => {
                state.status = 'failed';
                state.error = action.error.message || 'Something went wrong';
            })
            .addCase(downloadSong.pending, (state) => {
                state.status = 'loading';
            })
            .addCase(downloadSong.fulfilled, (state, action) => {
                state.status = 'succeeded';
                state.currentSong = action.payload.song;
            })
            .addCase(downloadSong.rejected, (state, action) => {
                state.status = 'failed';
                state.error = action.error.message || 'Failed to download song';
            })
            .addCase(fetchNextVideo.pending, (state) => {
                state.status = 'loading';
            })
            .addCase(fetchNextVideo.fulfilled, (state, action) => {
                state.status = 'succeeded';
                state.nextSong = action.payload;
            })
            .addCase(fetchNextVideo.rejected, (state, action) => {
                state.status = 'failed';
                state.error = action.error.message || 'Failed to fetch next song';
            });
    },
});

export const { setSearchTerm } = searchSlice.actions;
export default searchSlice.reducer;
