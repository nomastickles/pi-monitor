import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import Slider from "@mui/material/Slider";
import React from "react";
import "./App.css";
import * as actions from "./actions";
import { useAppDispatch } from "./hooks/useAppDispatch";
import { AtmosphereRow } from "./types";
import { useAppState } from "./hooks/useAppState";
import functionPlot from "function-plot";
import FormGroup from "@mui/material/FormGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import Switch from "@mui/material/Switch";
import AtmosphereTable from "./AtmosphereTable";
import Equalizer from "./Equalizer";
import { useIsDemoMode } from "./hooks/useIsDemoMode";
import { useUpdateDataToServer } from "./hooks/useUpdateDataToServer";
import MicIcon from "@mui/icons-material/Mic";

const DEFAULT_LOGARITHMIC_MULTIPLIER = 60;
const DEFAULT_LOUDNESS_BASE = -50;

const CURRENT_DATA_FETCH_INTERVAL = 5000;

function App() {
  const { isDemo } = useIsDemoMode();
  const { appData, fetchCurrentDataTrigger } = useAppState();
  const dispatch = useAppDispatch();
  const updateDataToServer = useUpdateDataToServer();
  const logMultiplierValue = Number(
    appData.DATA_LOUDNESS_SENSITIVITY || DEFAULT_LOGARITHMIC_MULTIPLIER
  );
  const logarithmicEquation = `log10(x)*${logMultiplierValue}`;
  const key = `${appData["KEY"]}`;
  const isUsingLogarithmic = Number(appData.DATA_LOUDNESS_SENSITIVITY) !== 0;

  const getCurrentInfo = React.useCallback(async () => {
    var url = new URL(`${window.location.origin}/current`);
    url.search = new URLSearchParams({
      key,
    }).toString();

    try {
      const response = await fetch(url.toString());
      const data = await response.json();

      dispatch(
        actions.setAppData({
          dataName: "DATA_LOUDNESS",
          data: data?.DATA_LOUDNESS,
        })
      );
      dispatch(
        actions.setAppData({
          dataName: "DATA_ATMOSPHERE",
          data: data?.DATA_ATMOSPHERE,
        })
      );
    } catch (e) {
      console.error(e);
    }

    dispatch(actions.initiateFetchCurrentData());
  }, [dispatch, key]);

  React.useEffect(() => {
    if (isDemo) {
      return;
    }
    if (!fetchCurrentDataTrigger) {
      // start things going / only happens once
      dispatch(actions.initiateFetchCurrentData());
      return;
    }

    setTimeout(() => {
      getCurrentInfo();
    }, CURRENT_DATA_FETCH_INTERVAL);
  }, [fetchCurrentDataTrigger, dispatch, getCurrentInfo, isDemo]);

  React.useEffect(() => {
    if (!isUsingLogarithmic) {
      return;
    }
    functionPlot({
      target: "#function-plot",
      width: 400,
      height: 400,
      yAxis: {
        label: "Resulting Brightness",
        domain: [0, 255],
      },
      xAxis: {
        label: "Brightness",
        domain: [0, 255],
      },
      data: [
        {
          fn: logarithmicEquation,
        },
      ],
      disableZoom: true,
      grid: true,
    });
  }, [logarithmicEquation, isUsingLogarithmic]);

  const atmosphereRows: AtmosphereRow[] = [];
  if (appData.DATA_ATMOSPHERE) {
    atmosphereRows.push({
      name: "Inside",
      tempC: appData.DATA_ATMOSPHERE.TEMP_C,
      tempF: appData.DATA_ATMOSPHERE.TEMP_F,
      humidity: appData.DATA_ATMOSPHERE.HUMIDITY,
    });
  }

  if (appData.DATA_ATMOSPHERE_OUTSIDE) {
    atmosphereRows.push({
      name: "Outside",
      tempC: appData.DATA_ATMOSPHERE_OUTSIDE.TEMP_C,
      tempF: appData.DATA_ATMOSPHERE_OUTSIDE.TEMP_F,
      humidity: appData.DATA_ATMOSPHERE_OUTSIDE.HUMIDITY,
    });
  }

  return (
    <div className="App">
      <header className="App-header">
        <Box sx={{ width: "85%", maxWidth: 400, mt: 2 }}>
          <AtmosphereTable rows={atmosphereRows} />
          <Typography gutterBottom variant="h5">
            <Stack direction="row" spacing={1}>
              <MicIcon sx={{ color: "#1976d2", fontSize: "1.7em" }} />
              <Box sx={{ ml: 0, pr: 1 }}>
                <Equalizer />
              </Box>
              <div>{appData.DATA_LOUDNESS || "?"} dB</div>
            </Stack>
          </Typography>
          <Box sx={{ m: 4 }} />

          <Typography gutterBottom>Mic Threshold dB</Typography>
          <Box sx={{ m: 3 }} />
          <Slider
            aria-label="Loudness"
            marks={[
              {
                value: -80,
                label: "-80 dB",
              },
              {
                value: 0,
                label: "0 dB",
              },
            ]}
            value={Number(appData.DATA_LOUDNESS_BASE || DEFAULT_LOUDNESS_BASE)}
            valueLabelDisplay="on"
            min={-80}
            max={0}
            onChange={(event: any) => {
              dispatch(
                actions.setAppData({
                  dataName: "DATA_LOUDNESS_BASE",
                  data: event.target.value,
                })
              );
              updateDataToServer("DATA_LOUDNESS_BASE", event.target.value);
            }}
          />
          <Box sx={{ m: 3 }} />
          <Typography gutterBottom>Night Vision Level</Typography>
          <Box sx={{ m: 3 }} />
          <Slider
            aria-label="Night Vision Level"
            marks={[
              {
                value: 0,
                label: "0",
              },
              {
                value: 255,
                label: "255",
              },
            ]}
            value={Number(appData.DATA_NIGHT_VISION_LEVEL || 0)}
            valueLabelDisplay="off"
            min={0}
            max={255}
            onChange={(event: any) => {
              dispatch(
                actions.setAppData({
                  dataName: "DATA_NIGHT_VISION_LEVEL",
                  data: event.target.value,
                })
              );
              updateDataToServer("DATA_NIGHT_VISION_LEVEL", event.target.value);
            }}
          />
          <Box sx={{ m: 3 }} />
          <FormGroup>
            <FormControlLabel
              control={<Switch checked={isUsingLogarithmic} />}
              label="Mic Logarithmic Factor"
              onChange={(_, checked) => {
                let value = !checked ? 0 : DEFAULT_LOGARITHMIC_MULTIPLIER;

                dispatch(
                  actions.setAppData({
                    dataName: "DATA_LOUDNESS_SENSITIVITY",
                    data: value,
                  })
                );
                updateDataToServer("DATA_LOUDNESS_SENSITIVITY", `${value}`);
              }}
            />
          </FormGroup>
          <Box sx={{ m: 5 }} />

          <Slider
            disabled={!isUsingLogarithmic}
            aria-label="log"
            value={logMultiplierValue}
            valueLabelDisplay="on"
            min={1}
            max={200}
            onChange={(event: any) => {
              dispatch(
                actions.setAppData({
                  dataName: "DATA_LOUDNESS_SENSITIVITY",
                  data: event.target.value,
                })
              );
              updateDataToServer(
                "DATA_LOUDNESS_SENSITIVITY",
                event.target.value
              );
            }}
          />
          <Typography gutterBottom>{logarithmicEquation}</Typography>
          <Box sx={{ ml: -4 }}>
            <div id="function-plot"></div>
          </Box>
        </Box>
      </header>
    </div>
  );
}

export default App;
