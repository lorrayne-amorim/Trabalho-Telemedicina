import sqlite3
from typing import List, Optional
from models.Medico import Medico
from sql.MedicoSql import *
from util.bancodedados import criar_conexao

class MedicoRepo:
    @classmethod
    def criar_tabela(cls) -> bool:
        try:
            with criar_conexao() as conexao:
                conexao.execute(SQL_CRIAR_TABELA)
                return True
        except sqlite3.Error:
            return False

    @classmethod
    def inserir(cls, medico: dict) -> Optional[Medico]:
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_INSERIR, (medico["nome"], medico["email"], medico["senha"], medico["crm"], ""))
                medico_obj = Medico(
                    id=cursor.lastrowid,
                    nome=medico["nome"],
                    email=medico["email"],
                    senha=medico["senha"],
                    crm=medico["crm"],
                    token=""
                )
                return medico_obj
        except sqlite3.Error:
            return None

    @classmethod
    def obter_todos(cls) -> List[Medico]:
        with criar_conexao() as conexao:
            cursor = conexao.cursor()
            tuplas = cursor.execute(SQL_OBTER_TODOS).fetchall()
            return [Medico(*t) for t in tuplas]

    @classmethod
    def obter_por_id(cls, id: int) -> Optional[Medico]:
        with criar_conexao() as conexao:
            tupla = conexao.cursor().execute(SQL_OBTER_POR_ID, (id,)).fetchone()
            return Medico(*tupla) if tupla else None

    @classmethod
    def obter_por_email(cls, email: str) -> Optional[Medico]:
        try:
            with criar_conexao() as conexao:
                tupla = conexao.cursor().execute(SQL_OBTER_POR_EMAIL, (email,)).fetchone()
                return Medico(*tupla) if tupla else None
        except sqlite3.Error:
            return None

    @classmethod
    def obter_por_token(cls, token: str) -> Optional[Medico]:
        try:
            with criar_conexao() as conexao:
                tupla = conexao.cursor().execute(SQL_OBTER_POR_TOKEN, (token,)).fetchone()
                return Medico(*tupla) if tupla else None
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
