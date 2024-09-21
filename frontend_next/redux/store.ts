import { configureStore } from "@reduxjs/toolkit";
import searchReducer from "./slices/searchSlice";
import videoReducer from "./slices/videoSlice";
import audioReducer from "./slices/audioSlice";


const store = configureStore({
    reducer: {
        search: searchReducer,
        video: videoReducer,
        audio: audioReducer,
        
    },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
export default store;
