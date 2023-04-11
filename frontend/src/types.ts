export type AppDataNames =
  | "LOUDNESS"
  | "LOUDNESS_BASE"
  | "LOUDNESS_SENSITIVITY"
  | "KEY"
  | "ATMOSPHERE"
  | "ATMOSPHERE_OUTSIDE";

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
