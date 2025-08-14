import React from 'react';
import ReactDOM from 'react-dom/client';
import { CssBaseline, Typography, Box, Stack } from '@mui/material';
import { FileUpload } from './modules/FileUpload';
import { DataTable } from './modules/DataTable';
import { TransformPanel } from './modules/TransformPanel';
import { useBackend } from './modules/useBackend';

const App: React.FC = () => {
  const backend = useBackend();

  return (
    <>
      <CssBaseline />
      <Box sx={{display:'flex', flexDirection:'column', height:'100vh', width:'100vw', overflow:'hidden'}}>
        <Box sx={{p:2, flexShrink:0}}>
          <Typography variant="h4" gutterBottom>Universal Data Processor</Typography>
          <FileUpload onSessionCreated={backend.handleSessionCreated} loading={backend.loading} />
        </Box>
        <Box sx={{flex:1, display:'flex', minHeight:0, overflow:'hidden', gap:2, px:2, pb:2}}>
          <Box sx={{width:360, flexShrink:0, overflowY:'auto', borderRight: '1px solid', borderColor:'divider', pr:2}}>
            <TransformPanel backend={backend} />
          </Box>
          <Box sx={{flex:1, minWidth:0, overflow:'hidden'}}>
            <DataTable rows={backend.rows} columns={backend.columns} maxWidthPx={Infinity} />
          </Box>
        </Box>
      </Box>
    </>
  );
};

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(<App />);
