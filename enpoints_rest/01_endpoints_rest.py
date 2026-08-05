from fastapi import FastAPI

app = FastAPI()

# Decorador @app.get()
# Función que atiende la solicitud GET a la ruta raíz "/"
# Respuesta automática en formato JSON con un mensaje de confirmación 
@app.get("/")
def home():
    return {"message": "API funcionando correctamente"}

@app.get("/items/{item_id}")
def get_employee(item_id: int):
    return {"employee_id": item_id}

# Decorador @app.post()
# Función que atiende la solicitud POST a la ruta "/employees"
# Respuesta automática en formato JSON con un mensaje de confirmación
@app.post("/employees")
def create_employee(employee: dict):
    return {"message": "Empleado registrado correctamente",
            "employee": employee}

# @Decorador @app.put()
# Función que atiende la solicitud PUT a la ruta "/employees/{employee_id}"
# Respuesta automática en formato JSON con un mensaje de confirmación y los datos del empleado actualizado
@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, employee: dict):
    return {"message": "Empleado actualizado correctamente",
            "employee_id": employee_id,
            "employee": employee}

# Decorador @app.delete()
# Función que atiende la solicitud DELETE a la ruta "/employees/{employee_id}"
# Respuesta automática en formato JSON con un mensaje de confirmación y el ID del empleado eliminado
@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    return {"message": "Empleado eliminado correctamente",
            "employee_id": employee_id}