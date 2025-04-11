import sqlite3
from typing import List, Optional
from models.Consulta import Consulta
from sql.ConsultaSql import *
from util.bancodedados import criar_conexao

class ConsultaRepo:
    @classmethod
    def criar_tabela(cls) -> bool:
        try:
            with criar_conexao() as conexao:
                conexao.execute(SQL_CRIAR_TABELA)
                return True
        except sqlite3.Error:
            return False

    @classmethod
    def inserir(cls, consulta: Consulta) -> Optional[Consulta]:
        try:
            with criar_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_INSERIR, (consulta.dia, consulta.hora, consulta.especialidadeMed))
                consulta.id = cursor.lastrowid
                return consulta
        except sqlite3.Error:
            return None

    @classmethod
    def obter_todos(cls) -> List[Consulta]:
        with criar_conexao() as conexao:
            cursor = conexao.cursor()
            tuplas = cursor.execute(SQL_OBTER_TODOS).fetchall()
            return [Consulta(*t) for t in tuplas]

    @classmethod
    def obter_por_id(cls, id: int) -> Optional[Consulta]:
        with criar_conexao() as conexao:
            tupla = conexao.cursor().execute(SQL_OBTER_POR_ID, (id,)).fetchone()
            return Consulta(*tupla) if tupla else None
