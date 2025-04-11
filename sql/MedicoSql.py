SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS medico (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        nome     TEXT    NOT NULL,
        email    TEXT    NOT NULL,
        senha    TEXT    NOT NULL,
        crm      TEXT    NOT NULL,
        token    TEXT
    )
"""

SQL_INSERIR = """
    INSERT INTO medico (nome, email, senha, crm, token)
    VALUES (?, ?, ?, ?, ?)
"""

SQL_ALTERAR = """
    UPDATE medico
    SET nome = ?, email = ?, senha = ?, crm = ?, token = ?
    WHERE id = ?
"""

SQL_EXCLUIR = """
    DELETE FROM medico
    WHERE id = ?
"""

SQL_OBTER_TODOS = """
    SELECT id, nome, email, senha, crm, token
    FROM medico
    ORDER BY nome
"""

SQL_OBTER_POR_ID = """
    SELECT id, nome, email, senha, crm, token
    FROM medico
    WHERE id = ?
"""

SQL_OBTER_POR_EMAIL = """
    SELECT id, nome, email, senha, crm, token
    FROM medico
    WHERE email = ?
"""

SQL_OBTER_POR_TOKEN = """
    SELECT id, nome, email, senha, crm, token
    FROM medico
    WHERE token = ?
"""

SQL_ATUALIZAR_TOKEN = """
    UPDATE medico
    SET token = ?
    WHERE id = ?
"""
