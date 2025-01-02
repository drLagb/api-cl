from fastapi import APIRouter
from src.routes.price.priceService import PriceService
from fastapi.responses import JSONResponse, PlainTextResponse

priceRouter = APIRouter(prefix="/price")

priceService = PriceService()

@priceRouter.get("/{id}/{material}/{thickness}/{amount}")
def get_price(id:str, material:str, thickness:str, amount:int):
    return priceService.get_price(id, material, thickness, amount, JSONResponse)

@priceRouter.get("/price/{reference}/{mount}")
async def getPriceSha256(reference:str, mount:str):
    return priceService.getPriceSha256(reference, mount, PlainTextResponse)