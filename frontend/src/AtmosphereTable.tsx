import * as React from "react";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableRow from "@mui/material/TableRow";
// import Paper from "@mui/material/Paper";
import { AtmosphereRow } from "./types";
import Box from "@mui/material/Box";

interface AtmosphereTableProps {
  rows: AtmosphereRow[];
}

export default function AtmosphereTable(props: AtmosphereTableProps) {
  const { rows } = props;
  if (!rows.length) return null;
  return (
    <>
      <TableContainer>
        <Table sx={{ width: "100%" }} aria-label="simple table" size="small">
          <TableBody>
            {rows.map((row) => (
              <TableRow
                key={row.name}
                sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
              >
                <TableCell component="th" scope="row">
                  {row.name}
                </TableCell>
                <TableCell align="right">{row.tempC} C</TableCell>
                <TableCell align="right">{row.tempF} F</TableCell>
                <TableCell align="right">{row.humidity} %</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <Box sx={{ m: 1 }} />
      <hr />
      <Box sx={{ m: 3 }} />
    </>
  );
}
