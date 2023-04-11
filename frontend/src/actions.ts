import { createAction } from "@reduxjs/toolkit";
import { SetAppDataProps, AppData } from "./types";

export const reset = createAction("reset");

export const initiateFetchCurrentData = createAction(
  "initiateFetchCurrentData"
);

export const setAppData = createAction<SetAppDataProps>("setAppData");
export const setAppDataAll = createAction<AppData>("setAppDataAll");
