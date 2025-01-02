from src.utils import filesPath, fiat, integrityKey
from src.utils.dfx import DXFAnalyzer, MaterialLibrary, Material, Calculator
from src.utils.errors import MaterialNotExistException
from src.routes.price.entity import PriceEntity
from hashlib import sha256
from math import ceil
from os import path
from fastapi import status
class PriceService:
    
    def __init__(self):
        self.MATERIALS:MaterialLibrary = MaterialLibrary()
    
    def get_price(self, id:str, material:str, thickness:str, amount:int, JSONResponse):
        try:
            thickness = thickness.replace("x", "/")
            filePath = path.join(filesPath, f"{id}.dxf")
            dxf = DXFAnalyzer(filePath, verifible=False)
            info:Material = self.MATERIALS.get_material(material, thickness)
            if info == None:
                info = MaterialLibrary.get_material_from_dicts(material, thickness)
                if info == None:
                    raise MaterialNotExistException()
                self.MATERIALS.add_material(info)
            calculator = Calculator(dxf, self.MATERIALS)
            price:float = ceil(calculator.calculate_price(info, amount)*100)
            return JSONResponse(
                content=PriceEntity(
                    id, 
                    calculator.dxf_analyzer.getArea(), 
                    price,
                    calculator.dxf_analyzer.calculate_perimeter(),
                    ""
                ).__dict__, status_code=status.HTTP_200_OK)
        except Exception as e:
            raise e
        
    async def getPriceSha256(self, reference:str, mount:str, PlainTextResponse):
        try:
            mensage = f"{reference}{mount}{fiat}{integrityKey}"
            return PlainTextResponse(content=sha256(mensage.encode()).hexdigest(), status_code=status.HTTP_200_OK)
        except Exception as e:
            raise e