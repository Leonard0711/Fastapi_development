from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
import os

# Creación de la conexion a la base de datos MySQL
PASSWORD = os.getenv("MYSQL_PASSWORD")
URL_DATABASE = f"mysql+mysqlconnector://leonardo:{PASSWORD}@localhost/Prueba"
engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class RegisterModel(Base):
    __tablename__ = "Registers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    edad = Column(Integer, nullable=False)

class RegistersRequest(BaseModel):
    nombre: str
    edad: int

class RegistersResponse(BaseModel):
    mensaje: str
    id: int
    nombre: str
    edad: int

app = FastAPI()

# Create
@app.post("/resgistro/", response_model=RegistersResponse)
def create_register(data: RegistersRequest, db: Session=Depends(get_db)):
    register = RegisterModel(nombre=data.nombre, edad=data.edad)
    db.add(register)
    db.commit()
    db.refresh(register)
    return {"mensaje": "Registro creado correctamente",
            "id": register.id,
            "nombre": register.nombre,
            "edad": register.edad}

# Read
@app.get("/registros/{registro_id}", response_model=RegistersResponse)
def get_register(registro_id: int, db: Session=Depends(get_db)):
    register = db.query(RegisterModel).filter(RegisterModel.id == registro_id).first()
    if register is None:
        raise HTTPException(status_code=401, detail="Registro no encontrado")
    return {"mensaje": "Registro encontrado",
            "id": register.id,
            "nombre": register.nombre,
            "edad": register.edad}

# Update
@app.put("/registros/{registro_id}", response_model=RegistersResponse)
def update_register(registro_id: int, new_data: RegistersRequest, db: Session=Depends(get_db)):
    register = db.query(RegisterModel).filter(RegisterModel.id == registro_id).first()
    if register is None:
        raise HTTPException(status_code=401, detail="Registro no encontrado")
    register.nombre = new_data.nombre
    register.edad = new_data.edad
    db.commit()
    db.refresh(register)
    return {"mensaje": "Registro actualizado correctamente",
            "id": register.id,
            "nombre": register.nombre,
            "edad": register.edad}

# Delete
@app.delete("/registros/{registro_id}", response_model=RegistersResponse)
def delete_register(registro_id, db: Session=Depends(get_db)):
    register = db.query(RegisterModel).filter(RegisterModel.id == registro_id).first()
    if register is None:
        raise HTTPException(status_code=401, detail="Registro no encontrado")
    db.delete(register)
    db.commit()
    return {"mensaje": "Registro eliminado correctamente",
            "id": register.id,
            "nombre": register.nombre,
            "edad": register.edad}