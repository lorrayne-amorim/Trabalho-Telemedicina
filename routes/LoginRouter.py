from fastapi import APIRouter, Depends, HTTPException, Request, Query, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from repositories.PacienteRepo import PacienteRepo
from repositories.MedicoRepo import MedicoRepo
from util.seguranca import conferir_senha, criar_token
from util.mensagem import redirecionar_com_mensagem

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/login")
async def get_login(request: Request, tipo: str = Query(...)):
    if tipo == "medico":
        return templates.TemplateResponse("medico/login_medico.html", {"request": request})
    elif tipo == "paciente":
        return templates.TemplateResponse("paciente/login_paciente.html", {"request": request})
    else:
        raise HTTPException(status_code=400, detail="Tipo inválido")

@router.post("/login")
async def post_login(request: Request, tipo: str = Query(...), email: str = Form(...), senha: str = Form(...)):
    # Lógica de login para Médico ou Paciente
    if tipo == "medico":
        medico = MedicoRepo.obter_por_email(email)
        if medico and conferir_senha(senha, medico.senha):
            token = criar_token(medico.id, "medico")
            response = RedirectResponse(url="/medico/dashboard", status_code=303)
            response.set_cookie(key="auth_token", value=token, httponly=True)
            return response
    elif tipo == "paciente":
        paciente = PacienteRepo.obter_por_email(email)
        if paciente and conferir_senha(senha, paciente.senha):
            token = criar_token(paciente.id, "paciente")
            response = RedirectResponse(url="/paciente/dashboard", status_code=303)
            response.set_cookie(key="auth_token", value=token, httponly=True)
            return response
    else:
        raise HTTPException(status_code=400, detail="Tipo inválido")
    
    # Se chegou aqui, login falhou
    if tipo == "medico":
        return templates.TemplateResponse("medico/login_medico.html", {"request": request, "erro": "Email ou senha incorretos"})
    else:
        return templates.TemplateResponse("paciente/login_paciente.html", {"request": request, "erro": "Email ou senha incorretos"})

@router.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie(key="auth_token")
    return response
