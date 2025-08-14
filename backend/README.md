# Backend (FastAPI)

Run the API:

```bash
uvicorn backend.app.main:app --reload
```

Endpoints:
- `POST /files/upload` - Upload CSV/XLSX
- `POST /transform/session` - Create session from JSON rows
- `GET /transform/session/{id}` - Get session data
- `POST /transform/keep-columns`
- `POST /transform/drop-columns`
- `POST /transform/rename-column`
- `POST /transform/pivot`
- `POST /transform/produce-output`
- `POST /transform/delta`
