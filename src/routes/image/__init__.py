from fastapi import APIRouter, UploadFile
from src.routes.image.imageService import ImageService
from fastapi.responses import JSONResponse, FileResponse

imageRouter = APIRouter(prefix="/image")

imageService = ImageService()

@imageRouter.get("/{id}")
def get_image(id:str):
    return imageService.get_image(id, FileResponse, JSONResponse)

@imageRouter.delete("/{id}")
def delete_image(id:str):
    return imageService.delete_image(id, JSONResponse)


@imageRouter.post("")
async def create_image(uploaded: UploadFile):
    return await imageService.create_image(uploaded, JSONResponse)
