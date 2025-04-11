SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS paciente (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        nome     TEXT    NOT NULL,
        email    TEXT    NOT NULL,
        senha    TEXT    NOT NULL,
        token    TEXT,
        cpf      TEXT    NOT NULL
    )
"""

SQL_INSERIR = """
    INSERT INTO paciente (nome, email, senha, token, cpf)
    VALUES (?, ?, ?, ?, ?)
"""

SQL_ALTERAR = """
    UPDATE paciente
    SET nome = ?, email = ?, senha = ?, token = ?, cpf = ?
    WHERE id = ?
"""

SQL_EXCLUIR = """
    DELETE FROM paciente
    WHERE id = ?
"""

SQL_OBTER_TODOS = """
    SELECT id, nome, email, senha, token, cpf
    FROM paciente
    ORDER BY nome
"""

SQL_OBTER_POR_ID = """
    SELECT id, nome, email, senha, token, cpf
    FROM paciente
    WHERE id = ?
"""

SQL_OBTER_POR_EMAIL = """
    SELECT id, nome, email, senha, token, cpf
    FROM paciente
    WHERE email = ?
"""

SQL_OBTER_POR_TOKEN = """
    SELECT id, nome, email, senha, token, cpf
    FROM paciente
    WHERE token = ?
"""

SQL_ATUALIZAR_TOKEN = """
    UPDATE paciente
    SET token = ?
    WHERE id = ?
"""
