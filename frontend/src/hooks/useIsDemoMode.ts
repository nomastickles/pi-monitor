import React from "react";
import { useAppDispatch } from "./useAppDispatch";
import * as actions from "../actions";

const isDemo = !!process.env.REACT_APP_IS_DEMO;

console.log("process.env", process.env);

export const useIsDemoMode = () => {
  const dispatch = useAppDispatch();

  // just to show things off

  React.useEffect(() => {
    if (!isDemo) {
      return;
    }

    dispatch(
      actions.setAppDataAll({
        KEY: "not-secure",
        DATA_ATMOSPHERE: {
          HUMIDITY: 51.4,
          TEMP_C: 22.1,
          TEMP_F: 71.8,
        },
        DATA_ATMOSPHERE_OUTSIDE: {
          HUMIDITY: 86,
          TEMP_C: 11.1,
          TEMP_F: 52,
        },
        DATA_LOUDNESS: "-38.38",
        DATA_LOUDNESS_BASE: "-37",
        DATA_LOUDNESS_SENSITIVITY: "110",
      })
    );
  }, [dispatch]);

  return {
    isDemo,
  };
};
