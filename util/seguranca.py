import secrets
from typing import Optional
import bcrypt
from fastapi import Request
from models.Paciente import Paciente
from models.Medico import Medico
from repositories.PacienteRepo import PacienteRepo
from repositories.MedicoRepo import MedicoRepo

def hash_senha(senha: str) -> str:
    try:
        hashed = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
        return hashed.decode()
    except ValueError:
        return ""

def conferir_senha(senha: str, hash_senha: str) -> bool:
    try:
        return bcrypt.checkpw(senha.encode(), hash_senha.encode())
    except ValueError:
        return False

def gerar_token(length: int = 32) -> str:
    try:
        return secrets.token_hex(length)
    except ValueError:
        return ""

def criar_token(usuario_id: int, tipo: str) -> str:
    token = gerar_token()
    if tipo == "paciente":
        PacienteRepo.atualizar_token(usuario_id, token)
    elif tipo == "medico":
        MedicoRepo.atualizar_token(usuario_id, token)
    return token

def adicionar_cookie_autenticacao(response, token):
    response.set_cookie(key="auth_token", value=token, max_age=1800, httponly=True, samesite="lax")
    return response

def excluir_cookie_autenticacao(response):
    response.delete_cookie(key="auth_token")
    return response

async def obter_usuario_logado(request: Request) -> Optional[Paciente | Medico]:
    try:
        token = request.cookies.get("auth_token")
        if not token or token.strip() == "":
            return None

        usuario = PacienteRepo.obter_por_token(token)
        if usuario:
            return usuario

        usuario = MedicoRepo.obter_por_token(token)
        return usuario
    except Exception:
        return None

async def atualizar_cookie_autenticacao(request: Request, call_next):
    response = await call_next(request)
    usuario = await obter_usuario_logado(request)
    if usuario:
        token = request.cookies.get("auth_token")
        response.set_cookie(key="auth_token", value=token, max_age=1800, httponly=True, samesite="lax")
    return response
