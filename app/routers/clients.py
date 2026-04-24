# Los Endpoints (Controladores)
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from .. import models, schemas, database
from ..services import import_service

router = APIRouter(
    prefix="/clients",
    tags=["Clients"]
)

# GET /clients, me dice todos los clientes
@router.get("/", response_model=list[schemas.ClientOut])
def get_clients(db: Session = Depends(database.get_db)):
    
    clients = db.query(models.Client).all() # Trae todos los registros de esa tabla
    return clients

# GET /clients/{id}, busco clientes por ID
@router.get("/{id}", response_model=schemas.ClientOut)
def get_client(id: int, db: Session = Depends(database.get_db)):
    
    client = db.query(models.Client).filter(models.Client.customer_id == id).first() # Filter me sirve para filtrar por condiciones, el first me da el primer resultado
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return client

# PUT /clients/{id}, acutalizo los datos de un cliente tomando como parametro su id
@router.put("/{id}", response_model=schemas.ClientOut)
def update_client(id: int, client_update: schemas.ClientUpdate, db: Session = Depends(database.get_db)):
    client_query = db.query(models.Client).filter(models.Client.customer_id == id) # Mismo metodo que usamos antes
    db_client = client_query.first()
    
    if not db_client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # el .dict me permite que python cree un diccionario con las llaves nombre, pais, etc.
    update_data = client_update.dict(exclude_unset=True) 
    
    client_query.update(update_data, synchronize_session=False)
    db.commit()
    
    return client_query.first()

# DELETE /clients/{id}, borro un cliente tomando como parametro su id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(id: int, db: Session = Depends(database.get_db)): # Devuelvo un 204, se borro de manera correcta
    client = db.query(models.Client).filter(models.Client.customer_id == id)
    
    if not client.first():
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    client.delete(synchronize_session=False)
    db.commit()
    return

@router.post("/import")
async def import_clients(file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    # Valido que me manden un archivo Excel
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="El archivo debe ser un Excel (.xlsx)")

    # Leemos el archivo
    contents = await file.read()
    
    # El paquete va al servicio para hacer el trabajo
    result = import_service.process_excel(contents, db)
    
    return result