from fastapi import APIRouter
from controllers.task_controller import router as task_router
from controllers.websocket import router as websocket_router
from controllers.auth_controller import router as auth_controller

router = APIRouter()
router.include_router(task_router)
router.include_router(websocket_router)
router.include_router(auth_controller)
