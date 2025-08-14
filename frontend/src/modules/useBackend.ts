import { useState, useCallback } from 'react';
import axios from 'axios';

const API_BASE = 'http://localhost:8000';

export interface BackendState {
  sessionId?: string;
  columns: string[];
  rows: any[];
  loading: boolean;
  handleSessionCreated: (file: File) => Promise<void>;
  keepColumns: (cols: string[]) => Promise<void>;
  dropColumns: (cols: string[]) => Promise<void>;
  renameColumn: (oldName: string, newName: string) => Promise<void>;
  pivot: (target: string, value: string) => Promise<void>;
  produceOutput: (cols: string[]) => Promise<void>;
  delta: (col1: string, col2: string, threshold: number) => Promise<void>;
  refresh: () => Promise<void>;
}

export function useBackend(): BackendState {
  const [sessionId, setSessionId] = useState<string | undefined>();
  const [columns, setColumns] = useState<string[]>([]);
  const [rows, setRows] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchSession = useCallback(async (id: string) => {
    const { data } = await axios.get(`${API_BASE}/transform/session/${id}`);
    setColumns(data.columns);
    setRows(data.rows);
  }, []);

  const handleSessionCreated = useCallback(async (file: File) => {
    setLoading(true);
    try {
      const form = new FormData();
      form.append('file', file);
      const uploadRes = await axios.post(`${API_BASE}/files/upload`, form, { headers: { 'Content-Type': 'multipart/form-data' } });
      const { data: sessionRes } = await axios.post(`${API_BASE}/transform/session`, { data: uploadRes.data.rows });
      setSessionId(sessionRes.session_id);
      setColumns(sessionRes.columns);
      await fetchSession(sessionRes.session_id);
    } finally {
      setLoading(false);
    }
  }, [fetchSession]);

  const op = useCallback(async (url: string, body: any) => {
    if (!sessionId) return;
    setLoading(true);
    try {
      await axios.post(`${API_BASE}${url}`, { session_id: sessionId, ...body });
      await fetchSession(sessionId);
    } finally {
      setLoading(false);
    }
  }, [sessionId, fetchSession]);

  return {
    sessionId,
    columns,
    rows,
    loading,
    handleSessionCreated,
    keepColumns: (cols) => op('/transform/keep-columns', { columns: cols }),
    dropColumns: (cols) => op('/transform/drop-columns', { columns: cols }),
    renameColumn: (oldName, newName) => op('/transform/rename-column', { old_name: oldName, new_name: newName }),
    pivot: (target, value) => op('/transform/pivot', { target, value }),
    produceOutput: (cols) => op('/transform/produce-output', { columns: cols }),
    delta: (col1, col2, threshold) => op('/transform/delta', { col1, col2, threshold }),
    refresh: async () => { if (sessionId) await fetchSession(sessionId); }
  };
}
