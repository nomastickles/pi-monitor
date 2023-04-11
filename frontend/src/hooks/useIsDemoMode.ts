import React from "react";
import { useAppDispatch } from "./useAppDispatch";
import * as actions from "../actions";

const isDemo = !!process.env.REACT_APP_IS_DEMO;

export const useIsDemoMode = () => {
  const dispatch = useAppDispatch();

  // just to show things off

  React.useEffect(() => {
    if (!isDemo) {
      return;
    }

    dispatch(
      actions.setAppDataAll({
        ATMOSPHERE: {
          HUMIDITY: 51.4,
          TEMP_C: 22.1,
          TEMP_F: 71.8,
        },
        ATMOSPHERE_OUTSIDE: {
          HUMIDITY: 86,
          TEMP_C: 11.1,
          TEMP_F: 52,
        },
        KEY: "no-secure",
        LOUDNESS: "-38.38",
        LOUDNESS_BASE: "-37",
        LOUDNESS_SENSITIVITY: "110",
      })
    );
  }, [dispatch]);

  return {
    isDemo,
  };
};
