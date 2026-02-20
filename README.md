## BackEnd - Instrucciones

### crear un ambiente
python -m venv server

### activar el ambiente
source server/Scripts/activate

# desativar ambiente
deactivate

### Instalar dependencias:
pip install fastapi uvicorn sqlalchemy pydantic python-jose[cryptography] passlib bcrypt

### Ejecutar el backend:
uvicorn main:app --host 0.0.0.0 --port 8000 --reload