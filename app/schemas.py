from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class ClientBase(BaseModel): #Rechazo peticiones que esten incorrectas
    name: str = Field(..., min_length=1, description="El nombre no puede estar vacio")
    email: EmailStr # Valida automáticamente el formato de email
    country: str
    age: Optional[int] = Field(None, ge=18, description="Si se envia, debe ser >= 18")


class ClientCreate(ClientBase):
    customer_id: int



class ClientUpdate(ClientBase):
    pass 




class ClientOut(ClientBase):
    customer_id: int

    class Config:
        from_attributes = True # Basicamente le digo que lea los datos como objetos en vez de diccionarios
