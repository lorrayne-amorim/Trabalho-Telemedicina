from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from routes.PacienteRouter import router as pacienteRouter
from routes.MedicoRouter import router as medicoRouter
from routes.ConsultaRouter import router as consultaRouter
from routes.HomeRouter import router as homeRouter
from routes.LoginRouter import router as loginRouter
from routes.CadastroRouter import router as cadastroRouter

from repositories.PacienteRepo import PacienteRepo
from repositories.MedicoRepo import MedicoRepo
from repositories.ConsultaRepo import ConsultaRepo

from util.seguranca import atualizar_cookie_autenticacao
from util.excecoes import configurar_paginas_de_erro

# Criação de tabelas (evita erros se rodar mais de uma vez)
PacienteRepo.criar_tabela()
MedicoRepo.criar_tabela()
ConsultaRepo.criar_tabela()

# Criação do app FastAPI
app = FastAPI(
    title="MedLink - Sistema de Telemedicina",
    description="Plataforma para conectar médicos e pacientes através de consultas online",
    version="1.0.0"
)

# Middleware de autenticação via cookie
app.middleware("http")(atualizar_cookie_autenticacao)

# Tratamento customizado de erros
configurar_paginas_de_erro(app)

# Servir arquivos estáticos (como imagens e CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Inclusão das rotas
# Rotas públicas
app.include_router(homeRouter)
app.include_router(loginRouter)
app.include_router(cadastroRouter)

# Rotas protegidas
app.include_router(pacienteRouter)
app.include_router(medicoRouter)
app.include_router(consultaRouter)

# Execução em modo de desenvolvimento
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
