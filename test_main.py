import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app import models

# Creo un bd en memoria para no modificar la original
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# No creamos las tablas aquí, lo haremos antes de cada test

# Sobreescribo la base de datos real por la de prueba para que los tests usen esta
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db



client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    # Limpiamos la BD y la volvemos a crear antes de cada test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield

# Los Test

def test_read_main():
    """Prueba que la API esté viva en la raíz"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API funcionando correctamente"}

def test_read_clients_empty():
    """Prueba que la lista de clientes empiece vacía"""
    response = client.get("/clients/")
    assert response.status_code == 200
    assert response.json() == []

def test_create_and_read_client():
    """Prueba que podemos consultar un cliente si lo agregamos manualmente a la base de datos de prueba"""
    
    # Insertamos un cliente
    db = TestingSessionLocal()
    test_client = models.Client(customer_id=99, name="Test User", email="test@test.com", country="Testland", age=25)
    db.add(test_client)
    db.commit()
    db.close()

    # Hacemos la peticion a la API
    response = client.get("/clients/99")
    
    # Verifico los resultados
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@test.com"
