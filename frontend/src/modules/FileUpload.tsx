import React, { useRef } from 'react';
import { Button, Stack } from '@mui/material';

export const FileUpload: React.FC<{ onSessionCreated: (file: File) => void; loading: boolean; }> = ({ onSessionCreated, loading }) => {
  const inputRef = useRef<HTMLInputElement | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const allowed = ['.csv', '.xlsx', '.xls'];
    const lower = file.name.toLowerCase();
    if (!allowed.some(ext => lower.endsWith(ext))) {
      alert('Unsupported file type. Please select a CSV, XLSX, or XLS file.');
      return;
    }
    // Optional: size guard (e.g., 10GB)
    const maxBytes = 10000 * 1024 * 1024;
    if (file.size > maxBytes) {
      alert('File too large (max 10GB for preview).');
      return;
    }
    onSessionCreated(file);
  };

  return (
    <Stack direction="row" spacing={2}>
  <input ref={inputRef} type="file" hidden onChange={handleChange} accept=".csv,.xlsx,.xls" />
      <Button variant="contained" disabled={loading} onClick={() => inputRef.current?.click()}>Upload File</Button>
    </Stack>
  );
};
