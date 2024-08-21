from fastapi import APIRouter
from app.services import auth, tasks

router = APIRouter()
router.include_router(auth.router, prefix=auth.route)
router.include_router(tasks.router, prefix=tasks.route)
