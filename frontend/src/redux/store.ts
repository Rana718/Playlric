import { configureStore } from "@reduxjs/toolkit";
import searchReducer from "./features/searchSlice";


const store = configureStore({
    reducer: {
        search: searchReducer,
    },
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware({
            serializableCheck: {
                ignoredActions: ['search/downloadSong/fulfilled'],
                ignoredPaths: ['search.currentSong.file'] 
            }
        })
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

export default store;