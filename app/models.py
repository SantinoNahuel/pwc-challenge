# Las Entidades de la base de datos
from sqlalchemy import Column, Integer, String
from .database import Base

class Client(Base):
    __tablename__ = "clientes"

    # el id tiene que ser unico
    customer_id = Column(Integer, primary_key=True, index=True) 
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    country = Column(String, nullable=False)
    age = Column(Integer, nullable=True) # opcional
