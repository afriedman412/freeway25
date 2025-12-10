from fastapi import APIRouter

router = APIRouter()


@router.get("/hey")
def root():
    return {"message": "whatup"}
