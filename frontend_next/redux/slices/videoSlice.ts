import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface VideoState {
    url: string;
    title: string;
    thumbnail_url: string;
}

const initialState: VideoState = {
    url: '',
    title: '',
    thumbnail_url: '',
};

const videoSlice = createSlice({
    name: 'video',
    initialState,
    reducers: {
        setVideoDetails: (state, action: PayloadAction<VideoState>) => {
            state.url = action.payload.url;
            state.title = action.payload.title;
            state.thumbnail_url = action.payload.thumbnail_url;
        },
        resetVideoDetails: (state) => {
            state.url = '';
            state.title = '';
            state.thumbnail_url = '';
        },
    },
});

export const { setVideoDetails, resetVideoDetails } = videoSlice.actions;

export default videoSlice.reducer;
