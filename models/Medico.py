from dataclasses import dataclass
from typing import Optional

@dataclass
class Medico:
    id: Optional[int] = None
    nome: Optional[str] = None
    email: Optional[str] = None
    senha: Optional[str] = None
    crm: Optional[str] = None
    token: Optional[str] = None