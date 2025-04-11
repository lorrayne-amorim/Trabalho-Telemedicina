# routes/CadastroRouter.py
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from repositories.PacienteRepo import PacienteRepo
from repositories.MedicoRepo import MedicoRepo
from util.mensagem import redirecionar_com_mensagem
from util.seguranca import hash_senha

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/cadastro")
async def get_cadastro(request: Request):
    return templates.TemplateResponse("cadastro.html", {"request": request})

@router.post("/cadastro")
async def post_cadastro(
    request: Request,
    tipo: str = Form(...),
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    confirmar_senha: str = Form(...),
    cpf: str = Form(None),
    crm: str = Form(None),
):
    # Verificar se as senhas coincidem
    if senha != confirmar_senha:
        return templates.TemplateResponse(
            "cadastro.html", 
            {"request": request, "erro": "As senhas não coincidem"}
        )
    
    # Verificar se o email já está em uso
    if tipo == "paciente":
        if not cpf:
            return templates.TemplateResponse(
                "cadastro.html", 
                {"request": request, "erro": "CPF é obrigatório para pacientes"}
            )
            
        paciente_existente = PacienteRepo.obter_por_email(email)
        if paciente_existente:
            return templates.TemplateResponse(
                "cadastro.html", 
                {"request": request, "erro": "Este email já está cadastrado como paciente"}
            )
        
        # Criar novo paciente
        novo_paciente = {
            "nome": nome,
            "email": email,
            "senha": hash_senha(senha),
            "cpf": cpf
        }
        PacienteRepo.inserir(novo_paciente)
        return redirecionar_com_mensagem("/login?tipo=paciente", "Cadastro realizado com sucesso! Faça login para continuar.")
    
    elif tipo == "medico":
        if not crm:
            return templates.TemplateResponse(
                "cadastro.html", 
                {"request": request, "erro": "CRM é obrigatório para médicos"}
            )
            
        medico_existente = MedicoRepo.obter_por_email(email)
        if medico_existente:
            return templates.TemplateResponse(
                "cadastro.html", 
                {"request": request, "erro": "Este email já está cadastrado como médico"}
            )
        
        # Criar novo médico
        novo_medico = {
            "nome": nome,
            "email": email,
            "senha": hash_senha(senha),
            "crm": crm
        }
        MedicoRepo.inserir(novo_medico)
        return redirecionar_com_mensagem("/login?tipo=medico", "Cadastro realizado com sucesso! Faça login para continuar.")
    
    else:
        return templates.TemplateResponse(
            "cadastro.html", 
            {"request": request, "erro": "Tipo de usuário inválido"}
        ) 