import React from 'react';
import ReactDOM from 'react-dom/client';
import { CssBaseline, Container, Typography, Box, Stack } from '@mui/material';
import { FileUpload } from './modules/FileUpload';
import { DataTable } from './modules/DataTable';
import { TransformPanel } from './modules/TransformPanel';
import { useBackend } from './modules/useBackend';

const App: React.FC = () => {
  const backend = useBackend();

  return (
    <>
      <CssBaseline />
      <Container maxWidth="xl" sx={{py:4}}>
        <Typography variant="h4" gutterBottom>Data Processor</Typography>
        <Stack direction={{xs:'column', md:'row'}} spacing={4} alignItems="flex-start">
          <Box flex={1}>
            <FileUpload onSessionCreated={backend.handleSessionCreated} loading={backend.loading} />
            <Box mt={2}>
              <TransformPanel backend={backend} />
            </Box>
          </Box>
          <Box flex={3}>
            <DataTable rows={backend.rows} columns={backend.columns} />
          </Box>
        </Stack>
      </Container>
    </>
  );
};

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(<App />);
