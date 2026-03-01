# #FASE 1
# # from fastapi import FastAPI, Request
# # from fastapi.templating import Jinja2Templates

# # app = FastAPI(title="Mi Plataforma IDP", version="1.0")

# # # Configuramos la carpeta donde viven nuestras páginas web
# # templates = Jinja2Templates(directory="templates")

# # # La ruta principal ahora carga tu Dashboard
# # @app.get("/")
# # def leer_raiz(request: Request):
# #     return templates.TemplateResponse(
# #         "index.html", 
# #         {"request": request, "titulo": "Dashboard IDP", "version": "1.0"}
# #     )

# # # Mantenemos la API intacta por si otros sistemas quieren consultarla
# # @app.get("/api/estado")
# # def estado_sistema():
# #     return {"estado": "Operativo", "version": "1.0", "entorno": "Producción"}


# # ##FASE 2
# # import os
# # from fastapi import FastAPI, Request
# # from fastapi.templating import Jinja2Templates
# # from azure.identity import DefaultAzureCredential
# # from azure.mgmt.resource import ResourceManagementClient

# # app = FastAPI(title="Mi Plataforma IDP", version="1.1")
# # templates = Jinja2Templates(directory="templates")

# # @app.get("/")
# # def leer_raiz(request: Request):
# #     return templates.TemplateResponse(
# #         "index.html", 
# #         {"request": request, "titulo": "Dashboard IDP", "version": "1.1"}
# #     )

# # @app.get("/api/recursos")
# # def listar_recursos():
# #     try:
# #         # 1. Obtenemos el ID de suscripción de las variables de entorno
# #         subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
# #         if not subscription_id:
# #             return {"estado": "error", "detalle": "Falta configurar AZURE_SUBSCRIPTION_ID"}

# #         # 2. Autenticación nativa (Cero contraseñas)
# #         credential = DefaultAzureCredential()
        
# #         # 3. Cliente de Azure y consulta
# #         resource_client = ResourceManagementClient(credential, subscription_id)
# #         grupos = resource_client.resource_groups.list()
        
# #         # 4. Formateamos la respuesta
# #         lista_grupos = [{"nombre": g.name, "ubicacion": g.location} for g in grupos]
# #         return {"estado": "éxito", "recursos": lista_grupos}
        
# #     except Exception as e:
# #         return {"estado": "error", "detalle": str(e)}

# ##NUEVO 3

# import os
# from fastapi import FastAPI, Request
# from fastapi.templating import Jinja2Templates
# from azure.identity import DefaultAzureCredential
# from azure.mgmt.resource import ResourceManagementClient

# app = FastAPI(title="Mi Plataforma IDP", version="1.1")

# templates = Jinja2Templates(directory="templates")

# @app.get("/")
# def leer_raiz(request: Request):
# return templates.TemplateResponse(
# "index.html",
# {"request": request, "titulo": "Dashboard IDP", "version": "1.1"}
# )

# @app.get("/api/recursos")
# def listar_recursos():
# try:
# subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
# if not subscription_id:
# return {"estado": "error", "detalle": "Falta configurar la variable AZURE_SUBSCRIPTION_ID en Azure"}

import os
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient

app = FastAPI(title="Mi Plataforma IDP", version="1.1")

templates = Jinja2Templates(directory="templates")

@app.get("/")
def leer_raiz(request: Request):
    # ¡Estos 4 espacios a la izquierda de la palabra 'return' son vitales!
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "titulo": "Dashboard IDP", "version": "1.1"}
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