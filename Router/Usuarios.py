from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from Class.Usuarios import Usuarios
from Utils.decorator import http_decorator
from Config.db import get_db

usuarios_router = APIRouter()


@usuarios_router.post('/listar', tags=["Usuarios"], response_model=dict)
@http_decorator
def listar_kpis(request: Request, db: Session = Depends(get_db)):
    data = getattr(request.state, "json_data", {})
    return Usuarios(db).listar(data)


@usuarios_router.post('/guardar', tags=["Usuarios"], response_model=dict)
@http_decorator
def guardar_usuario(request: Request, db: Session = Depends(get_db)):
    data = getattr(request.state, "json_data", {})
    return Usuarios(db).guardar_usuario(data)


@usuarios_router.post('/inactivar', tags=["Usuarios"], response_model=dict)
@http_decorator
def inactivar_usuario(request: Request, db: Session = Depends(get_db)):
    data = getattr(request.state, "json_data", {})
    return Usuarios(db).inactivar_usuario(data)
