# Logica de validacion del Excel
import pandas as pd
from sqlalchemy.orm import Session
from pydantic import ValidationError
from .. import models, schemas

def process_excel(file_bytes: bytes, db: Session):
    # Primero vamos a chequear que el archivo sea un excel y tenga todas las columnas que nos piden
    summary = {"total_records": 0, "inserted": 0, "errors": 0} 
    error_details = [] 

    try:
        # Leo el Excel con Pandas para trabajarlo en memoria
        df = pd.read_excel(file_bytes, sheet_name='Clientes')
    except Exception as e:
        return {"error": "Error al leer el archivo"}

    # El archivo debe tener las columnas id, name, contry y age 
    required_columns = ['customer_id', 'name', 'email', 'country', 'age']
    if not all(col in df.columns for col in required_columns):
        return {"error": "El archivo no tiene las columnas exactas requeridas."}

    summary["total_records"] = len(df) 

    # Verificamos que los IDs no esten repetidos en la base de datos ni en el propio archivo Excel
    existing_ids = {client.customer_id for client in db.query(models.Client.customer_id).all()}
    ids_in_file = set()

    # Itero fila por fila
    for index, row in df.iterrows():
        row_errors = []
        c_id = row.get('customer_id')

        # Validamos que el ID no este vacio
        if pd.isna(c_id):
            error_details.append({"customer_id": "Desconocido", "errors": ["ID faltante"]})
            summary["errors"] += 1
            continue

        c_id = int(c_id)

        if c_id in existing_ids or c_id in ids_in_file:
            row_errors.append("El customer_id ya existe o está duplicado")
        else:
            ids_in_file.add(c_id)

        
        client_data = {
            "customer_id": c_id,
            "name": "" if pd.isna(row.get('name')) else row.get('name'),
            "email": "" if pd.isna(row.get('email')) else row.get('email'),
            "country": "" if pd.isna(row.get('country')) else row.get('country'),
            "age": None if pd.isna(row.get('age')) else row.get('age')
        }

        # Valido con Pydantic que los datos sean correctos
        try:
            valid_client = schemas.ClientCreate(**client_data)
        except ValidationError as e:
            
            for err in e.errors():
                campo = err["loc"][0] # Me marca en que campo fallo
                row_errors.append(f"Error en {campo}: {err['msg']}")

        # Guardamos o descartamos la fila
        if row_errors:
            # Si hay errores, no guardamos y sumamos al reporte
            error_details.append({"customer_id": c_id, "errors": row_errors}) 
            summary["errors"] += 1 
        else:
            # Si está todo OK, lo preparamos para guardar en la BD
            db_client = models.Client(**valid_client.dict())
            db.add(db_client)
            existing_ids.add(c_id)
            summary["inserted"] += 1 

    # Guardamos todos los clientes
    db.commit()

    # Devolvemos el JSON
    return {
        "summary": summary, 
        "error_details": error_details 
    }
