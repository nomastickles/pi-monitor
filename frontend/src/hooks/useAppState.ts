import React from "react";
import { StateContext } from "../context";

export const useAppState = () => {
  const state = React.useContext(StateContext);

  return state;
};
