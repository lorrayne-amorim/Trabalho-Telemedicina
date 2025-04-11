import sqlite3
from typing import List, Optional
from models.Paciente import Paciente
from sql.PacienteSql import *
from util.bancodedados import criar_conexao

class PacienteRepo:
    @classmethod
    def criar_tabela(cls) -> bool:
        try:
            with criar_conexao() as conexao:
                conexao.execute(SQL_CRIAR_TABELA)
                return True
        except sqlite3.Error:
            return False

    @classmethod
    def inserir(cls, paciente: dict) -> Optional[Paciente]:
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_INSERIR, (paciente["nome"], paciente["email"], paciente["senha"], "", paciente["cpf"]))
                paciente_obj = Paciente(
                    id=cursor.lastrowid,
                    nome=paciente["nome"],
                    email=paciente["email"],
                    senha=paciente["senha"],
                    token="",
                    cpf=paciente["cpf"]
                )
                return paciente_obj
        except sqlite3.Error:
            return None

    @classmethod
    def obter_todos(cls) -> List[Paciente]:
        with criar_conexao() as conexao:
            cursor = conexao.cursor()
            tuplas = cursor.execute(SQL_OBTER_TODOS).fetchall()
            return [Paciente(*t) for t in tuplas]

    @classmethod
    def obter_por_id(cls, id: int) -> Optional[Paciente]:
        with criar_conexao() as conexao:
            tupla = conexao.cursor().execute(SQL_OBTER_POR_ID, (id,)).fetchone()
            return Paciente(*tupla) if tupla else None

    @classmethod
    def obter_por_email(cls, email: str) -> Optional[Paciente]:
        try:
            with criar_conexao() as conexao:
                tupla = conexao.cursor().execute(SQL_OBTER_POR_EMAIL, (email,)).fetchone()
                return Paciente(*tupla) if tupla else None
        except sqlite3.Error:
            return None

    @classmethod
    def obter_por_token(cls, token: str) -> Optional[Paciente]:
        try:
            with criar_conexao() as conexao:
                tupla = conexao.cursor().execute(SQL_OBTER_POR_TOKEN, (token,)).fetchone()
                return Paciente(*tupla) if tupla else None
        except sqlite3.Error:
            return None

    @classmethod
    def atualizar_token(cls, id: int, token: str) -> bool:
        try:
            with criar_conexao() as conexao:
                conexao.execute(SQL_ATUALIZAR_TOKEN, (token, id))
                return True
        except sqlite3.Error:
            return False
