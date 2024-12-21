from fastapi import FastAPI, UploadFile
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, PlainTextResponse
from uuid import uuid4
from Refactorizacion import DXFAnalyzer, MaterialLibrary, Material, Calculator
from hashlib import sha256, md5
from math import ceil

MATERIALS:MaterialLibrary = MaterialLibrary()

app = FastAPI()

fiat = os.getenv("FIAT")
integrityKey = os.getenv("INTEGRITY_KEY")

if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Files")):
    os.mkdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Files"))

if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Images")):
    os.mkdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Images"))

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/price/{id}/{material}/{thickness}/{amount}")
def get_price(id:str, material:str, thickness:str, amount:int):
    thickness = thickness.replace("x", "/")
    filePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Files", f"{id}.dxf")
    dxf = DXFAnalyzer(filePath, verifible=False)
    info:Material = MATERIALS.get_material(material, thickness)
    if info == None:
        info = MaterialLibrary.get_material_from_dicts(material, thickness)
        print(material, thickness)
        if info == None:
            return JSONResponse(content={"message":"the material or the thickness not found"}, status_code=400)
        MATERIALS.add_material(info)
    calculator = Calculator(dxf, MATERIALS)
    price:float = ceil(calculator.calculate_price(info, amount)*100)
    print(price)
    return JSONResponse(content={"id":id, "price":price, "message":f"Area: {calculator.dxf_analyzer.getArea()}\nPerimetro: {calculator.dxf_analyzer.calculate_perimeter()}"}, status_code=200)
    

@app.get("/image/{id}")
def get_image(id:str):
    try:
        imagepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Images", f"{id}.jpg")
        if not os.path.exists(imagepath):
            return PlainTextResponse("pepe")
        return FileResponse(imagepath, status_code=200, filename="image.jpg", media_type="application/jpg")
    except Exception as e:
        return JSONResponse(content={"message":str(e)}, status_code=400)

@app.delete("/image/{id}")
def delete_image(id:str):
    try:
        imagepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Images", f"{id}.jpg")
        filePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Files", f"{id}.dxf")
        os.remove(imagepath)
        os.remove(filePath)
        return JSONResponse(content={"message":"successful"})
    except Exception as e:
        return JSONResponse(content={"message":str(e)}, status_code=400)


@app.post("/image")
async def create_image(uploaded: UploadFile):
    try:
        if uploaded == None:
            return JSONResponse(content={"message":"error, the file was not uploading"}, status_code=400)
        content = await uploaded.read()
        id = md5(content).hexdigest()
        filePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Files", f"{id}.dxf")
        imagepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Images", f"{id}.jpg")
        if os.path.exists(filePath):
            return JSONResponse(content={"message":"success", "id":id}, status_code=200)
        with open(filePath, "wb") as File:
            File.write(content)
        dxf = DXFAnalyzer(filePath)
        print("xd")
        dxf.draw_dxf(imagepath)
        return JSONResponse(content={"message":"success", "id":id}, status_code=200)
    except IOError as e:
        return JSONResponse(content={"message":"El formato no es compatible"}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"message":str(e)}, status_code=500)
    finally:
        if(os.path.exists(filePath) and not os.path.exists(imagepath)):
            os.remove(filePath)
    
@app.get("/price/{reference}/{mount}")
async def getPriceSha256(reference:str, mount:str):
    try:
        mensage = f"{reference}{mount}{fiat}{integrityKey}"
        return PlainTextResponse(content=sha256(mensage.encode()).hexdigest(), status_code=200)
    except Exception as e:
        return JSONResponse(content={"message":str(e)}, status_code=500)