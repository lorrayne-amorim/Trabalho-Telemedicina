SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS consulta (
        id               INTEGER PRIMARY KEY AUTOINCREMENT,
        dia              TEXT    NOT NULL,
        hora             TEXT    NOT NULL,
        especialidadeMed TEXT    NOT NULL
    )
"""

SQL_INSERIR = """
    INSERT INTO consulta (dia, hora, especialidadeMed)
    VALUES (?, ?, ?)
"""

SQL_ALTERAR = """
    UPDATE consulta
    SET dia = ?, hora = ?, especialidadeMed = ?
    WHERE id = ?
"""

SQL_EXCLUIR = """
    DELETE FROM consulta
    WHERE id = ?
"""

SQL_OBTER_TODOS = """
    SELECT id, dia, hora, especialidadeMed
    FROM consulta
    ORDER BY dia, hora
"""

SQL_OBTER_POR_ID = """
    SELECT id, dia, hora, especialidadeMed
    FROM consulta
    WHERE id = ?
"""
