from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
from typing import List
import logging

router = APIRouter()
logger = logging.getLogger(__name__)
if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO)

def debug_full_df(name: str, df: pd.DataFrame):
    """Log entire DataFrame (all rows/cols). Use ONLY for debugging."""
    try:
        with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', None, 'display.max_colwidth', None):
            dump = df.to_string()
        logger.info(f"\n==== DataFrame Dump: {name} shape={df.shape} ====\n{dump}\n==== End Dump ====")
    except Exception as e:  # noqa: BLE001
        logger.exception(f"Failed to dump DataFrame {name}: {e}")

# In-memory storage (replace with cache/DB in production)
# Each session will store a dict: { 'df': DataFrame, 'raw_rows': List[dict] }
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
    index_columns: List[str] | None = None  # optional explicit index columns

class ProduceOutputRequest(BaseModel):
    session_id: str
    columns: List[str]

class DeltaRequest(BaseModel):
    session_id: str
    col1: str
    col2: str
    threshold: float

class SetHeaderRowRequest(BaseModel):
    session_id: str
    header_row_index: int  # index within raw_rows list (0-based)

@router.post('/set-header-row')
async def set_header_row(req: SetHeaderRowRequest):
    entry = SESSIONS.get(req.session_id)
    if entry is None:
        raise HTTPException(404, 'Session not found')
    raw_rows = entry.get('raw_rows')
    if not raw_rows:
        raise HTTPException(400, 'Original raw rows not available for this session')
    if req.header_row_index < 0 or req.header_row_index >= len(raw_rows):
        raise HTTPException(400, 'header_row_index out of range')

    header_row = raw_rows[req.header_row_index]

    # Detect if we are in a 'single wide column' scenario: every row dict has exactly 1 key
    single_col_mode = all(len(r.keys()) == 1 for r in raw_rows)

    if single_col_mode:
        # Extract the only value per row (string line). If value is not string, coerce.
        def only_value(d):
            if not d:
                return ''
            return next(iter(d.values()))

        header_line = str(only_value(header_row))
        # Decide delimiter: prefer tab if present, else comma
        delimiter = '\t' if ('\t' in header_line and header_line.count('\t') >= header_line.count(',')) else ','
        import csv
        try:
            reader = csv.reader([header_line], delimiter=delimiter)
            new_columns = [c.strip() for c in next(reader)]
        except Exception as e:  # noqa: BLE001
            raise HTTPException(400, f'Failed to parse header line: {e}')
        if not new_columns:
            raise HTTPException(400, 'Parsed header produced no columns')

        data_rows = []
        for idx, r in enumerate(raw_rows):
            if idx <= req.header_row_index:
                continue
            line = str(only_value(r))
            if not line.strip():
                continue
            try:
                values = next(csv.reader([line], delimiter=delimiter))
            except Exception:
                # Fallback naive split
                values = line.split(delimiter)
            # Normalize length
            if len(values) < len(new_columns):
                    values.extend([''] * (len(new_columns) - len(values)))
            elif len(values) > len(new_columns):
                values = values[:len(new_columns)]
            data_rows.append(dict(zip(new_columns, values)))

        entry['df'] = pd.DataFrame(data_rows if data_rows else [], columns=new_columns)
        debug_full_df("after set-header-row (single_col_mode)", entry['df'])
        # Update raw_rows to reflect newly structured rows for potential subsequent operations
        entry['raw_rows'] = data_rows
        return {"columns": list(entry['df'].columns)}
    else:
        # Existing multi-column dict mode: treat header row's values list as new column names
        new_columns = [str(v) for v in header_row.values()]
        data_rows = []
        for i, row in enumerate(raw_rows):
            if i <= req.header_row_index:
                continue
            values = list(row.values())
            if len(values) < len(new_columns):
                    values.extend([''] * (len(new_columns) - len(values)))
            elif len(values) > len(new_columns):
                values = values[:len(new_columns)]
            data_rows.append(dict(zip(new_columns, values)))
    entry['df'] = pd.DataFrame(data_rows if data_rows else [], columns=new_columns)
    debug_full_df("after set-header-row (multi-col mode)", entry['df'])
    entry['raw_rows'] = data_rows
    return {"columns": list(entry['df'].columns)}

@router.post('/session')
async def create_session(payload: SessionCreate):
    df = pd.DataFrame(payload.data)
    session_id = str(len(SESSIONS) + 1)
    SESSIONS[session_id] = { 'df': df, 'raw_rows': payload.data }
    return {"session_id": session_id, "columns": list(df.columns)}

@router.get('/session/{session_id}')
async def get_session(session_id: str):
    entry = SESSIONS.get(session_id)
    if entry is None:
        raise HTTPException(404, 'Session not found')
    df = entry['df']
    # Sanitize for JSON (Starlette disallows NaN/Inf by default)
    import numpy as np
    # Return full dataframe (no row limit) – caution: large responses for big sessions
    preview = df.copy()
    preview.replace([np.inf, -np.inf], np.nan, inplace=True)
    preview = preview.where(~preview.isna(), None)
    rows = preview.to_dict(orient='records')
    return {"columns": list(df.columns), "rows": rows}

@router.post('/keep-columns')
async def keep_columns(req: KeepColumnsRequest):
    entry = SESSIONS.get(req.session_id)
    if entry is None:
        raise HTTPException(404, 'Session not found')
    df = entry['df']
    cols = [c for c in req.columns if c in df.columns]
    if not cols:
        raise HTTPException(400, 'No valid columns provided')
    df = df[cols]
    entry['df'] = df
    return {"columns": list(df.columns)}

@router.post('/drop-columns')
async def drop_columns(req: DropColumnsRequest):
    entry = SESSIONS.get(req.session_id)
    if entry is None:
        raise HTTPException(404, 'Session not found')
    df = entry['df']
    cols = [c for c in req.columns if c in df.columns]
    df = df.drop(columns=cols)
    entry['df'] = df
    return {"columns": list(df.columns)}

@router.post('/rename-column')
async def rename_column(req: RenameColumnRequest):
    entry = SESSIONS.get(req.session_id)
    if entry is None:
        raise HTTPException(404, 'Session not found')
    df = entry['df']
    if req.old_name not in df.columns:
        raise HTTPException(400, 'Old name not in columns')
    df = df.rename(columns={req.old_name: req.new_name})
    entry['df'] = df
    return {"columns": list(df.columns)}

@router.post('/pivot')
async def pivot(req: PivotRequest):
    entry = SESSIONS.get(req.session_id)
    if entry is None:
        raise HTTPException(404, 'Session not found')
    df = entry['df']
    if req.target not in df.columns or req.value not in df.columns:
        raise HTTPException(400, 'Invalid columns')
    if req.index_columns:
        missing = [c for c in req.index_columns if c not in df.columns]
        if missing:
            raise HTTPException(400, f"Index columns not found: {missing}")
        # Ensure target/value not accidentally included twice; remove them if present
        index_cols = [c for c in req.index_columns if c not in [req.target, req.value]]
        if not index_cols:
            raise HTTPException(400, 'No valid index columns after excluding target/value')
    else:
        index_cols = [c for c in df.columns if c not in [req.target, req.value]]
    try:
        debug_full_df("before pivot", df)
        pivoted = df.pivot_table(index=index_cols, columns=req.target, values=req.value, aggfunc='first').reset_index()
    except Exception as e:
        raise HTTPException(400, str(e))
    entry['df'] = pivoted
    debug_full_df("after pivot", pivoted)
    return {"columns": list(pivoted.columns)}

@router.post('/produce-output')
async def produce_output(req: ProduceOutputRequest):
    entry = SESSIONS.get(req.session_id)
    if entry is None:
        raise HTTPException(404, 'Session not found')
    df = entry['df']
    cols = [c for c in req.columns if c in df.columns]
    if not cols:
        raise HTTPException(400, 'No valid columns provided')
    def build_output(row):
        selected = []
        for c in cols:
            v = row[c]
            if pd.isna(v):
                continue
            s = str(v).strip()
            if not s or s == '0':
                continue
            selected.append(c)
        return ', '.join(selected)
    df['Output'] = df.apply(build_output, axis=1)
    entry['df'] = df
    return {"columns": list(df.columns)}

@router.post('/delta')
async def delta(req: DeltaRequest):
    entry = SESSIONS.get(req.session_id)
    if entry is None:
        raise HTTPException(404, 'Session not found')
    df = entry['df']
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
    entry['df'] = df
    return {"columns": list(df.columns)}
