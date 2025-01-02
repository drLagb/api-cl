from src.utils import imagesPath, filesPath
from src.utils.dfx import MaterialLibrary, DXFAnalyzer
from src.utils.errors import FileNotExistException
from os import path, remove
from hashlib import md5
from fastapi import status
class ImageService:
    
    def __init__(self):
        self.MATERIALS:MaterialLibrary = MaterialLibrary()
    
    def get_image(self, id:str, FileResponse, JSONResponse):
        try:
            imagepath = path.join(imagesPath, f"{id}.jpg")
            if not path.exists(imagepath):
                return FileNotExistException
            return FileResponse(
                    imagepath, 
                    status_code=status.HTTP_200_OK, 
                    filename="image.jpg", 
                    media_type="application/jpg"
                )
        except Exception as e:
            return JSONResponse(
                content={"message":str(e)}, 
                status_code=status.HTTP_400_BAD_REQUEST
                )
            
    def delete_image(self, id:str, JSONResponse):
        try:
            imagepath = path.join(imagesPath, f"{id}.jpg")
            filePath = path.join(filesPath, f"{id}.dxf")
            remove(imagepath)
            remove(filePath)
            return JSONResponse(
                content={"message":"successful"}, 
                status_code=status.HTTP_202_ACCEPTED
                )
        except Exception as e:
            return JSONResponse(
                content={"message":str(e)}, 
                status_code=status.HTTP_400_BAD_REQUEST
                )
            
    async def create_image(self, uploaded, JSONResponse):
        try:
            if uploaded == None:
                raise FileNotExistException()
            content = await uploaded.read()
            id = md5(content).hexdigest()
            filePath = path.join(filesPath, f"{id}.dxf")
            imagepath = path.join(imagesPath, f"{id}.jpg")
            if path.exists(filePath):
                return JSONResponse(
                    content={"message":"success", "id":id}, 
                    status_code=status.HTTP_200_OK
                    )
            with open(filePath, "wb") as File:
                File.write(content)
            dxf = DXFAnalyzer(filePath)
            dxf.draw_dxf(imagepath)
            return JSONResponse(
                content={"message":"success", "id":id}, 
                status_code=status.HTTP_201_CREATED
                )
        except IOError as e:
            return JSONResponse(
                content={"message":"El formato no es compatible"}, 
                status_code=status.HTTP_406_NOT_ACCEPTABLE
                )
        except Exception as e:
            return JSONResponse(
                content={"message":str(e)}, 
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        finally:
            if(path.exists(filePath) and not path.exists(imagepath)):
                remove(filePath)