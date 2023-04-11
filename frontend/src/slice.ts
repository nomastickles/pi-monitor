import { createSlice } from "@reduxjs/toolkit";
import * as actions from "./actions";
import { AppState } from "./types";

export const initialState: AppState = {
  appData: window.APP_DATA_INIT || {},
  fetchCurrentDataTrigger: undefined,
};

export const AppSlice = createSlice({
  name: "app",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder.addCase(actions.setAppData, (state, { payload }) => {
      if (payload.clear) {
        state.appData[payload.dataName] = undefined;
        return;
      }
      const newValue = payload.data;
      state.appData[payload.dataName] = newValue;
    });

    builder.addCase(actions.reset, (state) => {
      state.appData = {};
    });
    builder.addCase(actions.initiateFetchCurrentData, (state) => {
      state.fetchCurrentDataTrigger = Date.now();
    });
    builder.addCase(actions.setAppDataAll, (state, { payload }) => {
      state.appData = { ...payload };
    });
  },
});
