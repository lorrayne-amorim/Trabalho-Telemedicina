from dataclasses import dataclass
from typing import Optional

@dataclass
class Consulta:
    id: Optional[int] = None
    dia: Optional[str] = None         # Ex: "2025-04-10"
    hora: Optional[str] = None        # Ex: "14:30"
    especialidadeMed: Optional[str] = None