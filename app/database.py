# Conexión a SQLite
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite guarda todo en este archivo local en la raíz de tu proyecto
SQLALCHEMY_DATABASE_URL = "sqlite:///./clientes.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} # Para permitir la conexión desde diferentes puertos (React en puerto 3000)
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependencia para inyectar la sesión de la DB en los endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
