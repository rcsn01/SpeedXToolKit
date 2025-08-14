import React from 'react';
import { Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from '@mui/material';

interface Props {
  rows: any[];
  columns: string[];
}

export const DataTable: React.FC<Props> = ({ rows, columns }) => {
  if (!columns.length) {
    return <Typography variant="body1">No data loaded.</Typography>;
  }
  return (
    <TableContainer component={Paper} sx={{ maxHeight: 600 }}>
      <Table stickyHeader size="small">
        <TableHead>
          <TableRow>
            {columns.map(col => <TableCell key={col}>{col}</TableCell>)}
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row, idx) => (
            <TableRow key={idx}>
              {columns.map(col => <TableCell key={col}>{row[col]}</TableCell>)}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};
