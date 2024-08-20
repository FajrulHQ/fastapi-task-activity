from fastapi import APIRouter
from app.services import auth

router = APIRouter()
router.include_router(auth.router, prefix=auth.route)
