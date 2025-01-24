from fastapi import APIRouter, Depends
from config.settings import get_settings, Settings

base_router = APIRouter()

@base_router.get("/welcome")
async def welcome(app_settings : Settings = Depends(get_settings)):  # check the type of app_settings (settings class)

    project_name = app_settings.APP_NAME
    version = app_settings.APP_VERSION

    return {"message": f"Welcome to {project_name} {version}"}