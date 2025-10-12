from fastapi import APIRouter, HTTPException
from app.domain.models import AnalyzeRequest, AnalyzeResponse
from app.application.model_client import BETOModelClient
from app.core.logging_config import logger
from app.domain.vocabulario import VOCABULARIO

router = APIRouter(prefix="", tags=["BETO Service"])

model_client = BETOModelClient()


@router.on_event("startup")
def startup_event():
    logger.info("Iniciando BETO Service...")
    if model_client.check_health():
        logger.info("Conexión con modelo establecida")
    else:
        logger.warning("No se pudo conectar con el modelo")


@router.get("/health")
def health_check():
    model_available = model_client.check_health()
    return {
        "status": "healthy" if model_available else "degraded",
        "model_service_available": model_available
    }


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_text(request: AnalyzeRequest):
    logger.info(f"Solicitud de análisis: {request.text}")

    if not request.text.strip():
        raise HTTPException(status_code=400, detail="El campo 'text' es obligatorio.")

    if not model_client.is_available:
        if not model_client.check_health():
            raise HTTPException(
                status_code=503,
                detail="Servicio de modelo no disponible"
            )

    try:
        resultado = model_client.analizar_texto(request.text)
        logger.info(f"Resultado del modelo: {resultado}")

        vocab_oficial = set(VOCABULARIO.keys())
        modismos_filtrados = {
            palabra: significado
            for palabra, significado in resultado["modismos_detectados"].items()
            if palabra in vocab_oficial
        }

        detalles_filtrados = [
            d for d in resultado["modismos_detallados"]
            if d["palabra"] in vocab_oficial
        ]

        response = {
            "status": "success",
            "texto_original": resultado["texto_original"],
            "modismos_detectados": modismos_filtrados,
            "modismos_detallados": detalles_filtrados,
            "total_modismos": len(modismos_filtrados),
            "modelo_info": {
                "nombre": "BETO-Finetuned",
                "version": "1.0.0"
            }
        }

        logger.info(f"Respuesta enviada con {len(modismos_filtrados)} modismos")
        return response

    except Exception as e:
        logger.error(f"Error en análisis: {e}")
        raise HTTPException(status_code=500, detail=str(e))