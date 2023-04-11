import React from "react";
import { AppDataNames } from "../types";
import { useAppState } from "./useAppState";
import { useIsDemoMode } from "./useIsDemoMode";
import debounce from "lodash.debounce";

const DEBOUNCE_TIME = 1000;

export const useUpdateDataToServer = () => {
  const { appData } = useAppState();
  const { isDemo } = useIsDemoMode();
  const key = `${appData["KEY"]}`;

  return React.useRef(
    debounce((dataName: AppDataNames, data: string) => {
      if (isDemo) {
        return;
      }
      const url = new URL(`${window.location.origin}/update`);
      url.search = new URLSearchParams({
        [dataName]: data,
        key,
      }).toString();

      try {
        fetch(url.toString());
      } catch (e) {
        console.error(e);
      }
    }, DEBOUNCE_TIME)
  ).current;
};
