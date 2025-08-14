from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
from typing import List, Optional

router = APIRouter()

# In-memory storage (replace with cache/DB in production)
SESSIONS = {}

class SessionCreate(BaseModel):
    data: List[dict]

class KeepColumnsRequest(BaseModel):
    session_id: str
    columns: List[str]

class DropColumnsRequest(BaseModel):
    session_id: str
    columns: List[str]

class RenameColumnRequest(BaseModel):
    session_id: str
    old_name: str
    new_name: str

class PivotRequest(BaseModel):
    session_id: str
    target: str
    value: str

class ProduceOutputRequest(BaseModel):
    session_id: str
    columns: List[str]

class DeltaRequest(BaseModel):
    session_id: str
    col1: str
    col2: str
    threshold: float

@router.post('/session')
async def create_session(payload: SessionCreate):
    df = pd.DataFrame(payload.data)
    session_id = str(len(SESSIONS) + 1)
    SESSIONS[session_id] = df
    return {"session_id": session_id, "columns": list(df.columns)}

@router.get('/session/{session_id}')
async def get_session(session_id: str):
    df = SESSIONS.get(session_id)
    if df is None:
        raise HTTPException(404, 'Session not found')
    return {"columns": list(df.columns), "rows": df.head(100).to_dict(orient='records')}

@router.post('/keep-columns')
async def keep_columns(req: KeepColumnsRequest):
    df = SESSIONS.get(req.session_id)
    if df is None:
        raise HTTPException(404, 'Session not found')
    cols = [c for c in req.columns if c in df.columns]
    if not cols:
        raise HTTPException(400, 'No valid columns provided')
    df = df[cols]
    SESSIONS[req.session_id] = df
    return {"columns": list(df.columns)}

@router.post('/drop-columns')
async def drop_columns(req: DropColumnsRequest):
    df = SESSIONS.get(req.session_id)
    if df is None:
        raise HTTPException(404, 'Session not found')
    cols = [c for c in req.columns if c in df.columns]
    df = df.drop(columns=cols)
    SESSIONS[req.session_id] = df
    return {"columns": list(df.columns)}

@router.post('/rename-column')
async def rename_column(req: RenameColumnRequest):
    df = SESSIONS.get(req.session_id)
    if df is None:
        raise HTTPException(404, 'Session not found')
    if req.old_name not in df.columns:
        raise HTTPException(400, 'Old name not in columns')
    df = df.rename(columns={req.old_name: req.new_name})
    SESSIONS[req.session_id] = df
    return {"columns": list(df.columns)}

@router.post('/pivot')
async def pivot(req: PivotRequest):
    df = SESSIONS.get(req.session_id)
    if df is None:
        raise HTTPException(404, 'Session not found')
    if req.target not in df.columns or req.value not in df.columns:
        raise HTTPException(400, 'Invalid columns')
    index_cols = [c for c in df.columns if c not in [req.target, req.value]]
    try:
        pivoted = df.pivot_table(index=index_cols, columns=req.target, values=req.value, aggfunc='first').reset_index()
    except Exception as e:
        raise HTTPException(400, str(e))
    SESSIONS[req.session_id] = pivoted
    return {"columns": list(pivoted.columns)}

@router.post('/produce-output')
async def produce_output(req: ProduceOutputRequest):
    df = SESSIONS.get(req.session_id)
    if df is None:
        raise HTTPException(404, 'Session not found')
    cols = [c for c in req.columns if c in df.columns]
    if not cols:
        raise HTTPException(400, 'No valid columns provided')
    df['Output'] = df[cols].apply(lambda row: ', '.join(row.index[row.notna() & (row != 0)]), axis=1)
    SESSIONS[req.session_id] = df
    return {"columns": list(df.columns)}

@router.post('/delta')
async def delta(req: DeltaRequest):
    df = SESSIONS.get(req.session_id)
    if df is None:
        raise HTTPException(404, 'Session not found')
    for c in [req.col1, req.col2]:
        if c not in df.columns:
            raise HTTPException(400, f'Column {c} missing')
    df['delta'] = pd.to_numeric(df[req.col1], errors='coerce') - pd.to_numeric(df[req.col2], errors='coerce')
    if 'Output' in df.columns:
        for idx, row in df.iterrows():
            if abs(row['delta']) > req.threshold and isinstance(row['Output'], str):
                to_remove = req.col1 if row[req.col1] < row[req.col2] else req.col2
                new_out = ','.join([x for x in row['Output'].split(',') if x.strip() != to_remove])
                df.at[idx, 'Output'] = new_out
    SESSIONS[req.session_id] = df
    return {"columns": list(df.columns)}
