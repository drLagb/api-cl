from src.database.basemodel import TB_USUARIOS
from src.database.CRUD import session
from sqlalchemy import select, and_
from src.routes.user.dto import UserDto
from hashlib import sha256
from fastapi.encoders import jsonable_encoder

class UserService:
    
    def existUserByEmail(self, email:str)->bool:
        consult = select(TB_USUARIOS).where(TB_USUARIOS.Correo == email)
        information = session.execute(consult).scalars().all()
        for i in information:
            print(i)
        return True if(information) else False
    
    def createUser(self, user:UserDto)->None:
        session.add(
            TB_USUARIOS(
                Nombre=user.Nombre, 
                Correo=user.Correo,
                Direccion=user.Direccion,
                Contraseña=user.Contraseña
                ))
        session.commit()
        
    def getAllUsers(self)->TB_USUARIOS:
        consult = select(TB_USUARIOS)
        return session.execute(consult).scalars().all()
    
    def verifyUser(self, email:str, password:str)->bool:
        consult = select(TB_USUARIOS).where(TB_USUARIOS.Correo == email)
        user = session.execute(consult).scalars().one()
        return user.Contraseña == sha256(password).hexdigest()
    
    def getUser(self, email:str, password:str)->bool:
        consult = select(
                TB_USUARIOS.Nombre, 
                TB_USUARIOS.Correo, 
                TB_USUARIOS.Direccion
            ).where(
                and_(
                    TB_USUARIOS.Correo == email,
                    TB_USUARIOS.Contraseña == sha256(password.encode()).hexdigest()
                )
            )
        print(consult)
        user = session.execute(consult).fetchone()
        return {"nombre":user[0], "Correo":user[1], "Dirección": user[2]}
    
    def updateUser(self, user: UserDto)->None:
        consult = select(
                TB_USUARIOS
            ).where(
                and_(
                    TB_USUARIOS.Correo == user.Correo,
                    TB_USUARIOS.Contraseña == user.Contraseña
                )
            )
        print(consult)
        oldUser = session.execute(consult).scalars().one()
        print(oldUser)
        oldUser.Nombre = user.Nombre
        oldUser.Direccion = user.Direccion
        oldUser.Contraseña = user.Contraseña
        session.commit()