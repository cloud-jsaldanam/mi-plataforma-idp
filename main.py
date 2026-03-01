# # #FASE 1
# # # from fastapi import FastAPI, Request
# # # from fastapi.templating import Jinja2Templates

# # # app = FastAPI(title="Mi Plataforma IDP", version="1.0")

# # # # Configuramos la carpeta donde viven nuestras páginas web
# # # templates = Jinja2Templates(directory="templates")

# # # # La ruta principal ahora carga tu Dashboard
# # # @app.get("/")
# # # def leer_raiz(request: Request):
# # #     return templates.TemplateResponse(
# # #         "index.html", 
# # #         {"request": request, "titulo": "Dashboard IDP", "version": "1.0"}
# # #     )

# # # # Mantenemos la API intacta por si otros sistemas quieren consultarla
# # # @app.get("/api/estado")
# # # def estado_sistema():
# # #     return {"estado": "Operativo", "version": "1.0", "entorno": "Producción"}


# # # ##FASE 2
# # # import os
# # # from fastapi import FastAPI, Request
# # # from fastapi.templating import Jinja2Templates
# # # from azure.identity import DefaultAzureCredential
# # # from azure.mgmt.resource import ResourceManagementClient

# # # app = FastAPI(title="Mi Plataforma IDP", version="1.1")
# # # templates = Jinja2Templates(directory="templates")

# # # @app.get("/")
# # # def leer_raiz(request: Request):
# # #     return templates.TemplateResponse(
# # #         "index.html", 
# # #         {"request": request, "titulo": "Dashboard IDP", "version": "1.1"}
# # #     )

# # # @app.get("/api/recursos")
# # # def listar_recursos():
# # #     try:
# # #         # 1. Obtenemos el ID de suscripción de las variables de entorno
# # #         subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
# # #         if not subscription_id:
# # #             return {"estado": "error", "detalle": "Falta configurar AZURE_SUBSCRIPTION_ID"}

# # #         # 2. Autenticación nativa (Cero contraseñas)
# # #         credential = DefaultAzureCredential()
        
# # #         # 3. Cliente de Azure y consulta
# # #         resource_client = ResourceManagementClient(credential, subscription_id)
# # #         grupos = resource_client.resource_groups.list()
        
# # #         # 4. Formateamos la respuesta
# # #         lista_grupos = [{"nombre": g.name, "ubicacion": g.location} for g in grupos]
# # #         return {"estado": "éxito", "recursos": lista_grupos}
        
# # #     except Exception as e:
# # #         return {"estado": "error", "detalle": str(e)}

# # ##NUEVO 3

# # import os
# # from fastapi import FastAPI, Request
# # from fastapi.templating import Jinja2Templates
# # from azure.identity import DefaultAzureCredential
# # from azure.mgmt.resource import ResourceManagementClient

# # app = FastAPI(title="Mi Plataforma IDP", version="1.1")

# # templates = Jinja2Templates(directory="templates")

# # @app.get("/")
# # def leer_raiz(request: Request):
# # return templates.TemplateResponse(
# # "index.html",
# # {"request": request, "titulo": "Dashboard IDP", "version": "1.1"}
# # )

# # @app.get("/api/recursos")
# # def listar_recursos():
# # try:
# # subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
# # if not subscription_id:
# # return {"estado": "error", "detalle": "Falta configurar la variable AZURE_SUBSCRIPTION_ID en Azure"}

# import os
# from fastapi import FastAPI, Request
# from fastapi.templating import Jinja2Templates
# from azure.identity import DefaultAzureCredential
# from azure.mgmt.resource import ResourceManagementClient

# app = FastAPI(title="Mi Plataforma IDP", version="1.1")

# templates = Jinja2Templates(directory="templates")

# @app.get("/")
# def leer_raiz(request: Request):
#     # ¡Estos 4 espacios a la izquierda de la palabra 'return' son vitales!
#     return templates.TemplateResponse(
#         "index.html", 
#         {"request": request, "titulo": "Dashboard IDP", "version": "1.1"}
#     )

# @app.get("/api/recursos")
# def listar_recursos():
#     try:
#         subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
#         if not subscription_id:
#             return {"estado": "error", "detalle": "Falta configurar AZURE_SUBSCRIPTION_ID"}

#         credential = DefaultAzureCredential()
        
#         resource_client = ResourceManagementClient(credential, subscription_id)
#         grupos = resource_client.resource_groups.list()
        
#         lista_grupos = [{"nombre": g.name, "ubicacion": g.location} for g in grupos]
#         return {"estado": "éxito", "recursos": lista_grupos}
        
#     except Exception as e:
#         return {"estado": "error", "detalle": str(e)}

import os
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient

# Nuevas librerías para la Base de Datos
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

# --- 1. CONFIGURACIÓN DE BASE DE DATOS ---
DATABASE_URL = os.environ.get("DATABASE_URL")

# Si probamos en la laptop y no hay variable, usa una base de datos local temporal (SQLite)
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./idp_local.db" 

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- 2. MODELO DE DATOS (Nuestra Tabla) ---
class RegistroDespliegue(Base):
    __tablename__ = "despliegues"
    id = Column(Integer, primary_key=True, index=True)
    recurso = Column(String, index=True)
    estado = Column(String)
    fecha = Column(DateTime, default=datetime.utcnow)
    usuario = Column(String, default="admin")

# ¡Magia! Esto crea la tabla en PostgreSQL automáticamente si no existe
Base.metadata.create_all(bind=engine)

# --- 3. APLICACIÓN FASTAPI ---
app = FastAPI(title="Mi Plataforma IDP", version="2.0")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def leer_raiz(request: Request):
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "titulo": "Dashboard IDP - Nivel 2", "version": "2.0"}
    )

@app.get("/api/recursos")
def listar_recursos():
    try:
        subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
        if not subscription_id:
            return {"estado": "error", "detalle": "Falta configurar AZURE_SUBSCRIPTION_ID"}

        credential = DefaultAzureCredential()
        resource_client = ResourceManagementClient(credential, subscription_id)
        grupos = resource_client.resource_groups.list()
        
        lista_grupos = [{"nombre": g.name, "ubicacion": g.location} for g in grupos]
        return {"estado": "éxito", "recursos": lista_grupos}
    except Exception as e:
        return {"estado": "error", "detalle": str(e)}

# NUEVO: Endpoint para simular un despliegue y guardarlo en la Base de Datos
@app.post("/api/desplegar/{nombre_recurso}")
def simular_despliegue(nombre_recurso: str):
    db = SessionLocal()
    nuevo_registro = RegistroDespliegue(
        recurso=nombre_recurso,
        estado="Exitoso"
    )
    db.add(nuevo_registro)
    db.commit()
    db.close()
    return {"estado": "éxito", "mensaje": f"Recurso guardado en BD"}

# NUEVO: Endpoint para leer la Base de Datos
@app.get("/api/historial")
def obtener_historial():
    db = SessionLocal()
    # Traemos los últimos 10 despliegues ordenados por fecha
    registros = db.query(RegistroDespliegue).order_by(RegistroDespliegue.fecha.desc()).limit(10).all()
    db.close()
    return [{"id": r.id, "recurso": r.recurso, "estado": r.estado, "fecha": r.fecha.strftime("%Y-%m-%d %H:%M:%S")} for r in registros]