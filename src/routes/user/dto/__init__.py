from fastapi import FastAPI
from pydantic import BaseModel, Field, validator
from hashlib import sha256
from src.routes.user import userService

app = FastAPI()

class UserDto(BaseModel):
    Nombre: str = Field(
        ..., 
        max_length=256, 
        description="El nombre debe ser menor a 256 caracteres",
        examples=["alexander Guitierres"]
        )
    
    Contraseña: str = Field(
        ..., 
        max_length=32, 
        description="La contraseña debe ser menor a 32 caracteres",
        examples=["ContraseñaMuySegura123"]
        )
    
    Direccion: str = Field(
        ..., 
        max_length=256, 
        description="La dirección debe ser menor a 256 caracteres",
        examples=["Crr 8 n 8 59"]
        )
    
    Correo: str = Field(
        ..., 
        max_length=256, 
        description="El correo siempre debe ser diferente por usuario",
        examples=["correoNuevo@direccion.dominio"]
        )
    
    @validator('Contraseña')
    def passwordvalidation(cls, password:str):
        return sha256(password.encode()).hexdigest()