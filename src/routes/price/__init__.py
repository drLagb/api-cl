from fastapi import APIRouter
from src.routes.price.priceService import PriceService
from fastapi.responses import JSONResponse

priceRouter = APIRouter(prefix="/price")

priceService = PriceService()

@priceRouter.get("/{id}/{material}/{thickness}/{amount}")
def get_price(id:str, material:str, thickness:str, amount:int):
    return priceService.get_price(id, material, thickness, amount, JSONResponse)