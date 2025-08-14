from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
from io import BytesIO
from pathlib import Path  # added

router = APIRouter()

@router.post('/upload')
async def upload_file(file: UploadFile = File(...)):
    try:
        # Ensure a filename is present
        if not file.filename:
            raise HTTPException(status_code=400, detail='Missing filename in upload')

        ext = Path(file.filename).suffix.lower()

        content = await file.read()

        if ext == '.csv':
            df = pd.read_csv(BytesIO(content))
        elif ext in ('.xlsx', '.xls'):
            df = pd.read_excel(BytesIO(content), engine='openpyxl')
        else:
            raise HTTPException(status_code=400, detail='Unsupported file type')

        return {
            "filename": file.filename,
            "columns": list(df.columns),
            "rows": df.head(50).to_dict(orient='records'),
            "rowCount": len(df)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))