from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from models.Paciente import Paciente
from repositories.PacienteRepo import PacienteRepo
from util.mensagem import redirecionar_com_mensagem
from util.seguranca import obter_usuario_logado

router = APIRouter(prefix="/paciente")
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard")
async def dashboard_paciente(request: Request, usuario: Paciente = Depends(obter_usuario_logado)):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return templates.TemplateResponse("paciente/dashboard.html", {"request": request, "paciente": usuario})

@router.get("/inserir")
async def get_inserir_paciente(request: Request, usuario: Paciente = Depends(obter_usuario_logado)):
    if not usuario or not usuario.token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return templates.TemplateResponse("paciente/inserir.html", {"request": request, "usuario": usuario})

@router.post("/inserir")
async def post_inserir_paciente(
    nome: str = Form(...), email: str = Form(...), senha: str = Form(...), cpf: str = Form(...), token: str = Form(None),
    usuario: Paciente = Depends(obter_usuario_logado),
):
    if not usuario or not usuario.token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    paciente = Paciente(nome=nome, email=email, senha=senha, token=token, cpf=cpf)
    PacienteRepo.inserir(paciente)
    return redirecionar_com_mensagem("/paciente", "Paciente cadastrado com sucesso!")

@router.get("/prontuario")
async def prontuario_paciente(request: Request, usuario: Paciente = Depends(obter_usuario_logado)):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return templates.TemplateResponse("paciente/prontuario.html", {"request": request, "paciente": usuario})
