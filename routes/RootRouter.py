from fastapi import (APIRouter, Depends, Form, HTTPException, Path, Query, Request, status)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.Paciente import Paciente
from models.Medico import Medico
from repositories.PacienteRepo import PacienteRepo
from repositories.MedicoRepo import MedicoRepo
from repositories.ConsultaRepo import ConsultaRepo
from util.mensagem import adicionar_cookie_mensagem, redirecionar_com_mensagem
from util.seguranca import (adicionar_cookie_autenticacao, conferir_senha, excluir_cookie_autenticacao,
                            gerar_token, obter_hash_senha, obter_usuario_logado)

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def get_root(request: Request, usuario = Depends(obter_usuario_logado)):
    consultas = ConsultaRepo.obter_todos()
    return templates.TemplateResponse("root/index.html", {"request": request, "usuario": usuario, "consultas": consultas})


@router.get("/login")
async def get_login(request: Request, tipo: str = Query(...)):
    if tipo not in ["medico", "paciente"]:
        raise HTTPException(status_code=400, detail="Tipo inválido")

    return templates.TemplateResponse(f"login_{tipo}.html", {"request": request})


@router.post("/login", response_class=RedirectResponse)
async def post_login(email: str = Form(...), senha: str = Form(...), return_url: str = Query("/")):
    from repositories.PacienteRepo import PacienteRepo
    from repositories.MedicoRepo import MedicoRepo

    user = None
    tipo_usuario = None

    if PacienteRepo.existe_email(email):
        hash_senha = PacienteRepo.obter_senha_por_email(email)
        if conferir_senha(senha, hash_senha):
            user = PacienteRepo.obter_por_email(email)
            tipo_usuario = "paciente"
    elif MedicoRepo.existe_email(email):
        hash_senha = MedicoRepo.obter_senha_por_email(email)
        if conferir_senha(senha, hash_senha):
            user = MedicoRepo.obter_por_email(email)
            tipo_usuario = "medico"

    if user:
        token = gerar_token()
        if tipo_usuario == "paciente":
            PacienteRepo.alterar_token_por_email(token, user.email)
        elif tipo_usuario == "medico":
            MedicoRepo.alterar_token_por_email(token, user.email)

        response = RedirectResponse(return_url, status.HTTP_302_FOUND)
        adicionar_cookie_autenticacao(response, token)
        adicionar_cookie_mensagem(response, f"Login realizado com sucesso como {tipo_usuario}.")
        return response

    return redirecionar_com_mensagem("/login", "Email ou senha incorretos.")

@router.get("/logout")
async def get_logout(usuario = Depends(obter_usuario_logado)):
    if usuario:
        if PacienteRepo.existe_email(usuario.email):
            PacienteRepo.alterar_token_por_email("", usuario.email)
        elif MedicoRepo.existe_email(usuario.email):
            MedicoRepo.alterar_token_por_email("", usuario.email)

        response = RedirectResponse("/", status.HTTP_302_FOUND)
        excluir_cookie_autenticacao(response)
        adicionar_cookie_mensagem(response, "Saída realizada com sucesso.")
        return response
    return RedirectResponse("/")