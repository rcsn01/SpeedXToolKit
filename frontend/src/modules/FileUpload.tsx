import React, { useRef } from 'react';
import { Button, Stack } from '@mui/material';

export const FileUpload: React.FC<{ onSessionCreated: (file: File) => void; loading: boolean; }> = ({ onSessionCreated, loading }) => {
  const inputRef = useRef<HTMLInputElement | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) onSessionCreated(file);
  };

  return (
    <Stack direction="row" spacing={2}>
      <input ref={inputRef} type="file" hidden onChange={handleChange} accept=".csv,.xlsx" />
      <Button variant="contained" disabled={loading} onClick={() => inputRef.current?.click()}>Upload File</Button>
    </Stack>
  );
};
