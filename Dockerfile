# Usamos una imagen oficial y ligera de Python
FROM python:3.9-slim

# Creamos una carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiamos los archivos de requerimientos e instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto de nuestro código
COPY . .

# Exponemos el puerto de nuestra API
EXPOSE 8000

# Comando para arrancar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]