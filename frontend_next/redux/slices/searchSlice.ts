import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";


export const fetchSearchResults = createAsyncThunk(
  "search/fetchSearchResults",
  async (query: string) => {
      const response = await axios.post('http://localhost:8000/videos/search/', { query });
      return response.data;
  }
);


interface SeachState{
    results: Array<{
        url: string,
        title: string,
        image_url: string,
        duration: string,
    }>;
    status: "idle" | "loading" | "succeeded" | "failed";
}


const initialState: SeachState = {
    results: [],
    status: "idle",
};

const searchSlice = createSlice({
    name: "search",
    initialState,
    reducers: {},
    extraReducers: (builder) => {
        builder
            .addCase(fetchSearchResults.pending, (state) => {
                state.status = "loading";
            })
            .addCase(fetchSearchResults.fulfilled, (state, action) => {
                state.results = action.payload;
                state.status = "succeeded";
            })
            .addCase(fetchSearchResults.rejected, (state) => {
                state.status = "failed";
            })
    }
});


export default searchSlice.reducer;