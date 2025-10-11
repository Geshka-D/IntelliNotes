from fastapi import APIRouter

router = APIRouter()

@router.get("/me")
def get_me():
    # Placeholder user endpoint
    return {"id": 1, "name": "Demo user", "email": "demo@example.com"}
