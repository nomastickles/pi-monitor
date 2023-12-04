export type AppDataNames =
  | "KEY"
  | "DATA_LOUDNESS"
  | "DATA_LOUDNESS_BASE"
  | "DATA_LOUDNESS_SENSITIVITY"
  | "DATA_ATMOSPHERE"
  | "DATA_ATMOSPHERE_OUTSIDE"
  | "DATA_NIGHT_VISION_LEVEL";

export type AppData = Partial<Record<AppDataNames, any>>;

export type AppState = {
  appData: AppData;
  fetchCurrentDataTrigger?: number;
};

export interface SetAppDataProps {
  dataName: AppDataNames;
  data?: number;
  clear?: boolean;
}

declare global {
  interface Window {
    APP_DATA_INIT: AppData;
  }
}

export interface AtmosphereRow {
  name: string;
  tempC: string | number;
  tempF: string | number;
  humidity: string | number;
}
