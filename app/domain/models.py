from pydantic import BaseModel
from typing import Dict, List


class AnalyzeRequest(BaseModel):
    text: str


class ModismoDetalle(BaseModel):
    palabra: str
    significado_detectado: str
    contexto: str
    confianza: str


class AnalyzeResponse(BaseModel):
    status: str
    texto_original: str
    modismos_detectados: Dict[str, str]
    modismos_detallados: List[ModismoDetalle]
    total_modismos: int
    modelo_info: Dict[str, str]
