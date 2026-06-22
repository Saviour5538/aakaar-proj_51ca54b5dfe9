from fastapi import APIRouter

router = APIRouter(prefix="/tech_stack", tags=["Tech Stack"])

@router.get("/")
async def get_tech_stack():
    return {
        "language": "Python",
        "backend": "FastAPI",
        "frontend": "React/TypeScript",
        "database": "PostgreSQL",
        "orm": "SQLAlchemy"
    }