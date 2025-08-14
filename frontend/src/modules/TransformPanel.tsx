import React, { useState } from 'react';
import { BackendState } from './useBackend';
import { Box, Button, Stack, TextField, Typography, Autocomplete, Paper } from '@mui/material';

export const TransformPanel: React.FC<{ backend: BackendState }> = ({ backend }) => {
  const [keep, setKeep] = useState<string[]>([]);
  const [drop, setDrop] = useState<string[]>([]);
  const [renameOld, setRenameOld] = useState('');
  const [renameNew, setRenameNew] = useState('');
  const [pivotTarget, setPivotTarget] = useState('');
  const [pivotValue, setPivotValue] = useState('');
  const [pivotIndexCols, setPivotIndexCols] = useState<string[]>([]);
  const [outputCols, setOutputCols] = useState<string[]>([]);
  const [deltaCol1, setDeltaCol1] = useState('');
  const [deltaCol2, setDeltaCol2] = useState('');
  const [deltaThreshold, setDeltaThreshold] = useState(0);
  const [headerRowIndex, setHeaderRowIndex] = useState('');

  return (
    <Paper sx={{p:2}}>
      <Typography variant="h6" gutterBottom>Transformations</Typography>
      <Stack spacing={2}>
        <Stack direction="row" spacing={1}>
          <TextField label="Header Row Index" value={headerRowIndex} onChange={e=>setHeaderRowIndex(e.target.value)} sx={{width:180}} />
          <Button variant="outlined" disabled={!headerRowIndex || backend.loading} onClick={()=>backend.setHeaderRow(Number(headerRowIndex))}>Set Header Row</Button>
        </Stack>
  <Autocomplete multiple disableCloseOnSelect options={backend.columns} value={keep} onChange={(_,v)=>setKeep(v)} renderInput={(params)=><TextField {...params} label="Keep Columns" />} />
        <Button size="small" variant="contained" disabled={!keep.length || backend.loading} onClick={()=>backend.keepColumns(keep)}>Apply Keep</Button>

  <Autocomplete multiple disableCloseOnSelect options={backend.columns} value={drop} onChange={(_,v)=>setDrop(v)} renderInput={(params)=><TextField {...params} label="Drop Columns" />} />
        <Button size="small" variant="contained" disabled={!drop.length || backend.loading} onClick={()=>backend.dropColumns(drop)}>Apply Drop</Button>

        <Stack direction="row" spacing={1}>
          <Autocomplete options={backend.columns} value={renameOld} onChange={(_,v)=>setRenameOld(v||'')} renderInput={(p)=><TextField {...p} label="Old Name" />} sx={{flex:1}} />
          <TextField label="New Name" value={renameNew} onChange={e=>setRenameNew(e.target.value)} sx={{flex:1}} />
          <Button variant="outlined" disabled={!renameOld || !renameNew || backend.loading} onClick={()=>backend.renameColumn(renameOld, renameNew)}>Rename</Button>
        </Stack>

        <Stack spacing={1}>
          <Stack direction="row" spacing={1}>
            <Autocomplete options={backend.columns} value={pivotTarget} onChange={(_,v)=>setPivotTarget(v||'')} renderInput={(p)=><TextField {...p} label="Pivot Target" />} sx={{flex:1}} />
            <Autocomplete options={backend.columns} value={pivotValue} onChange={(_,v)=>setPivotValue(v||'')} renderInput={(p)=><TextField {...p} label="Pivot Value" />} sx={{flex:1}} />
          </Stack>
          <Autocomplete multiple disableCloseOnSelect options={backend.columns.filter(c=>c!==pivotTarget && c!==pivotValue)} value={pivotIndexCols} onChange={(_,v)=>setPivotIndexCols(v)} renderInput={(p)=><TextField {...p} label="Pivot Index Columns (optional)" />} />
          <Button variant="outlined" disabled={!pivotTarget || !pivotValue || backend.loading} onClick={()=>backend.pivot(pivotTarget, pivotValue, pivotIndexCols)}>Pivot</Button>
        </Stack>

        <Autocomplete multiple options={backend.columns} value={outputCols} onChange={(_,v)=>setOutputCols(v)} renderInput={(params)=><TextField {...params} label="Produce Output Columns" />} />
        <Button size="small" variant="contained" disabled={!outputCols.length || backend.loading} onClick={()=>backend.produceOutput(outputCols)}>Produce Output</Button>

        <Stack direction="row" spacing={1}>
          <Autocomplete options={backend.columns} value={deltaCol1} onChange={(_,v)=>setDeltaCol1(v||'')} renderInput={(p)=><TextField {...p} label="Delta Col 1" />} sx={{flex:1}} />
          <Autocomplete options={backend.columns} value={deltaCol2} onChange={(_,v)=>setDeltaCol2(v||'')} renderInput={(p)=><TextField {...p} label="Delta Col 2" />} sx={{flex:1}} />
          <TextField type="number" label="Threshold" value={deltaThreshold} onChange={e=>setDeltaThreshold(Number(e.target.value))} sx={{width:130}} />
          <Button variant="outlined" disabled={!deltaCol1 || !deltaCol2 || backend.loading} onClick={()=>backend.delta(deltaCol1, deltaCol2, deltaThreshold)}>Delta</Button>
        </Stack>
      </Stack>
    </Paper>
  );
};
