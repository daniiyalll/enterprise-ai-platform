// Point this at your running FastAPI backend.
// Default assumes: uvicorn app.main:app --reload  (runs on port 8000)
window.API_BASE = window.localStorage.getItem("api_base") || "http://127.0.0.1:8000/api/v1";
