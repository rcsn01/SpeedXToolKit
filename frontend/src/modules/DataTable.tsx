import React from 'react';
import { Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from '@mui/material';

interface Props {
  rows: any[];
  columns: string[];
  /** Optional maximum pixel width for the table (defaults 1600). */
  maxWidthPx?: number;
}

export const DataTable: React.FC<Props> = ({ rows, columns, maxWidthPx = 1600 }) => {
  if (!columns.length) {
    return <Typography variant="body1">No data loaded.</Typography>;
  }

  // Compute a min width so horizontal scroll appears when many columns
  const baseWidth = Math.max(800, columns.length * 140);
  const clampedWidth = Math.min(baseWidth, maxWidthPx);

  return (
    <TableContainer
      component={Paper}
      sx={{
        maxHeight: 600,
        overflow: 'auto',          // both directions
        width: '100%',
        maxWidth: '100%',
      }}
    >
      <Table
        stickyHeader
        size="small"
        sx={{
          width: clampedWidth,
          minWidth: clampedWidth, // ensure applied width
          tableLayout: 'auto'
        }}
      >
        <TableHead>
          <TableRow>
            <TableCell
              sx={{
                fontWeight: 600,
                position: 'sticky',
                left: 0,
                zIndex: 3,
                backgroundColor: 'background.paper'
              }}
            >
              #
            </TableCell>
            {columns.map(col => (
              <TableCell key={col} sx={{ whiteSpace: 'nowrap' }}>
                {col}
              </TableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row, idx) => (
            <TableRow key={idx} hover>
              <TableCell
                sx={{
                  color: 'text.secondary',
                  position: 'sticky',
                  left: 0,
                  backgroundColor: 'background.paper',
                  zIndex: 2
                }}
              >
                {idx}
              </TableCell>
              {columns.map(col => (
                <TableCell key={col}>
                  {row[col]}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};