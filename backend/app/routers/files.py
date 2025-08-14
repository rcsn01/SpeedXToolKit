from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
from io import BytesIO
from pathlib import Path
import logging
from pandas.errors import ParserError
# ...existing code...
logger = logging.getLogger(__name__)
router = APIRouter(tags=["files"])

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        if not file or not file.filename:
            raise HTTPException(status_code=400, detail="Missing filename in upload")

        ext = (Path(file.filename).suffix or "").lower()
        content = await file.read()
        size = len(content)
        if size == 0:
            raise HTTPException(status_code=400, detail="Empty file")

        logger.info(f"Received file name={file.filename} ext={ext} size={size} bytes")

        if ext == ".csv":
            df = None
            last_err = None
            # Attempts: default, python engine sniff, common delimiters
            attempts = [
                dict(),  # default
                dict(sep=None, engine="python"),
            ]
            for sep in [",", ";", "\t", "|"]:
                attempts.append(dict(sep=sep))
            for kw in attempts:
                try:
                    df = pd.read_csv(BytesIO(content), **kw)
                    break
                except (ParserError, UnicodeDecodeError) as e:
                    last_err = e
                    continue
            if df is None:
                raise HTTPException(
                    status_code=400,
                    detail=f"Could not parse CSV (tried default/sniff/common delimiters). Last error: {last_err}"
                )
        elif ext == ".xlsx":
            try:
                df = pd.read_excel(BytesIO(content), engine="openpyxl")
            except ImportError as e:
                raise HTTPException(status_code=500, detail=f"openpyxl not installed: {e}")
            except Exception as e:  # noqa: BLE001
                raise HTTPException(status_code=400, detail=f"Failed to read .xlsx file: {e}")
        elif ext == ".xls":
            # Use xlrd for legacy Excel format
            try:
                df = pd.read_excel(BytesIO(content), engine="xlrd")
            except ImportError as e:
                raise HTTPException(status_code=500, detail=f"xlrd not installed: {e}")
            except ValueError as e:
                # Some newer xlrd versions removed xls support; advise user
                raise HTTPException(status_code=400, detail=f"xlrd cannot read .xls: {e}")
            except Exception as e:  # noqa: BLE001
                raise HTTPException(status_code=400, detail=f"Failed to read .xls file: {e}")
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")

        # Return ALL rows (debug mode) – beware large payloads for big files
        return {
            "filename": file.filename,
            "columns": list(map(str, df.columns)),
            "rows": df.to_dict(orient="records"),
            "rowCount": int(len(df)),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("File upload failed")
        raise HTTPException(status_code=500, detail=f"Upload failed: {e}")