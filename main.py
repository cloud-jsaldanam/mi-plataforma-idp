from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Mi Plataforma IDP", version="1.0")

# Configuramos la carpeta donde viven nuestras páginas web
templates = Jinja2Templates(directory="templates")

# La ruta principal ahora carga tu Dashboard
@app.get("/")
def leer_raiz(request: Request):
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "titulo": "Dashboard IDP", "version": "1.0"}
    )

# Mantenemos la API intacta por si otros sistemas quieren consultarla
@app.get("/api/estado")
def estado_sistema():
    return {"estado": "Operativo", "version": "1.0", "entorno": "Producción"}