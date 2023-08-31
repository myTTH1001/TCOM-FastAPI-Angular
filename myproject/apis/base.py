from fastapi import APIRouter

from apis.v1 import route_user, route_blog, route_file, route_login
from apis.v2 import route_cache, route_system


api_router = APIRouter()
api_router.include_router(route_user.router,prefix="",tags=["users"])
api_router.include_router(route_blog.router,prefix="",tags=["blogs"])
api_router.include_router(route_file.router,prefix="",tags=["file"])
api_router.include_router(route_login.router, prefix="", tags=["login"])
api_router.include_router(route_cache.router, prefix="", tags=["cache"])
api_router.include_router(route_system.router, prefix="", tags=["system"])