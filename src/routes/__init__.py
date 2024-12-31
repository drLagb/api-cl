from fastapi import APIRouter
from src.routes.price import priceRouter as __priceRouter

routesRouter = APIRouter(prefix="")

routesRouter.include_router(__priceRouter)