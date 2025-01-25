from fastapi import APIRouter
from src.routes.user.userService import UserService
from fastapi.responses import JSONResponse, PlainTextResponse
from src.routes.user.dto import UserDto

userRouter = APIRouter(prefix="/user")

userService = UserService()

@userRouter.get("/{email}/{password}")
async def getUser(email:str, password:str):
    return userService.getUser(email, password)

@userRouter.get("/")
async def getAllUsers():
    return userService.getAllUsers()

@userRouter.post("/")
async def createUser(user: UserDto):
    return userService.createUser(user)

@userRouter.patch("/")
async def updateUser(user: UserDto):
    return userService.updateUser(user)