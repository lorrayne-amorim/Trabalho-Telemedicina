from fastapi import APIRouter, Depends, Form, HTTPException, Path, Request, status
from fastapi.templating import Jinja2Templates
from models.Paciente import Paciente
from models.Medico import Medico
from models.Consulta import Consulta
from repositories.ConsultaRepo import ConsultaRepo
from util.mensagem import redirecionar_com_mensagem
from util.seguranca import obter_usuario_logado

router = APIRouter(prefix="/consulta")
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_consultas(request: Request, usuario: Paciente | Medico = Depends(obter_usuario_logado)):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    consultas = ConsultaRepo.obter_todos()
    return templates.TemplateResponse("consulta/index.html", {"request": request, "usuario": usuario, "consultas": consultas})

@router.get("/inserir")
async def get_inserir_consulta(request: Request, usuario: Paciente | Medico = Depends(obter_usuario_logado)):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return templates.TemplateResponse("consulta/inserir.html", {"request": request, "usuario": usuario})

@router.post("/inserir")
async def post_inserir_consulta(
    dia: str = Form(...), hora: str = Form(...), especialidadeMed: str = Form(...),
    usuario: Paciente | Medico = Depends(obter_usuario_logado),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    consulta = Consulta(dia=dia, hora=hora, especialidadeMed=especialidadeMed)
    ConsultaRepo.inserir(consulta)
    return redirecionar_com_mensagem("/consulta", "Consulta cadastrada com sucesso!")