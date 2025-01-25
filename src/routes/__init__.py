from fastapi import APIRouter
from src.routes.price import priceRouter as __priceRouter
from src.routes.image import imageRouter as __imageRouteer
from src.routes.user import userRouter as __userRouter

routesRouter = APIRouter(prefix="")

routesRouter.include_router(__priceRouter)
routesRouter.include_router(__imageRouteer)
routesRouter.include_router(__userRouter)