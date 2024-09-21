// redux/slices/audioSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface AudioState {
  fileUrl: string;
  isPlaying: boolean;
  currentTime: number;
}

const initialState: AudioState = {
  fileUrl: '',
  isPlaying: false,
  currentTime: 0,
};

const audioSlice = createSlice({
  name: 'audio',
  initialState,
  reducers: {
    setFileUrl: (state, action: PayloadAction<string>) => {
      state.fileUrl = action.payload;
    },
    setIsPlaying: (state, action: PayloadAction<boolean>) => {
      state.isPlaying = action.payload;
    },
    setCurrentTime: (state, action: PayloadAction<number>) => {
      state.currentTime = action.payload;
    },
  },
});

export const { setFileUrl, setIsPlaying, setCurrentTime } = audioSlice.actions;
export default audioSlice.reducer;
