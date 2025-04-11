from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from models.Medico import Medico
from repositories.MedicoRepo import MedicoRepo
from util.mensagem import redirecionar_com_mensagem
from util.seguranca import obter_usuario_logado

router = APIRouter(prefix="/medico")
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard")
async def dashboard_medico(request: Request, usuario: Medico = Depends(obter_usuario_logado)):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return templates.TemplateResponse("medico/dashboard.html", {"request": request, "medico": usuario})

@router.get("/inserir")
async def get_inserir_medico(request: Request, usuario: Medico = Depends(obter_usuario_logado)):
    if not usuario or not usuario.token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return templates.TemplateResponse("medico/inserir.html", {"request": request, "usuario": usuario})

@router.post("/inserir")
async def post_inserir_medico(
    nome: str = Form(...), email: str = Form(...), senha: str = Form(...), crm: str = Form(...), token: str = Form(None),
    usuario: Medico = Depends(obter_usuario_logado),
):
    if not usuario or not usuario.token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    medico = Medico(nome=nome, email=email, senha=senha, crm=crm, token=token)
    MedicoRepo.inserir(medico)
    return redirecionar_com_mensagem("/medico", "Médico cadastrado com sucesso!")
