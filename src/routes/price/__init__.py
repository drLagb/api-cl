from fastapi import APIRouter
from src.routes.price.priceService import PriceService
from fastapi.responses import JSONResponse, PlainTextResponse
from src.utils import db_user

priceRouter = APIRouter(prefix="/price")

priceService = PriceService()

@priceRouter.get("/{id}/{material}/{thickness}/{amount}")
def get_price(id:str, material:str, thickness:str, amount:int):
    return priceService.get_price(id, material, thickness, amount, JSONResponse)

@priceRouter.get("/{reference}/{mount}")
async def getPriceSha256(reference:str, mount:str):
    return await priceService.getPriceSha256(reference, mount, PlainTextResponse)