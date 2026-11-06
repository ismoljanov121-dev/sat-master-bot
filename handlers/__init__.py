from aiogram import Router

from handlers.admin import router as admin_router
from handlers.menu import router as menu_router

router = Router()
# The menu router ends with a catch-all for private messages, so admin commands must come first.
router.include_router(admin_router)
router.include_router(menu_router)
