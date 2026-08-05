from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

# Creación de modelos con BaseModel de Pydantic
class UserRequest(BaseModel):
    username: str
    age: int

@app.get("/users")
def create_user(user: UserRequest):
    return user

# Validacion con Field (restriccion de valores)
# VÁLIDO
# {"username": "leo",
#  "age": 30}

# NO VÁLIDO
# {"username": "ab", 
#  "age": 15}
from pydantic import BaseModel, Field

class UserRequest1(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    age: int = Field(ge=18, le=100)

# Validaciom de URL con HttpUrl
from pydantic import HttpUrl

class Website(BaseModel):
    url: HttpUrl

# Parámetros opciones con Optional
from typing import Optional

class UserRequest2(BaseModel):
    phone: Optional[str] = None

# Validación del Response (response_model)
class UserResponse(BaseModel):
    id: int
    username: str

@app.post("/users", response_model = UserResponse)
def create_user(user: UserRequest):
    return {"id": 1, "username": user.username}