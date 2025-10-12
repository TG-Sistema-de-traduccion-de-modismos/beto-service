import requests
from app.core.config import settings
from app.core.logging_config import logger
from typing import Dict, Any


class BETOModelClient:
    def __init__(self):
        self.base_url = settings.model_service_url
        self.is_available = False
    
    def check_health(self) -> bool:
        try:
            response = requests.get(
                f"{self.base_url}/health",
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                self.is_available = data.get("model_loaded", False)
                logger.info(f"Modelo disponible: {self.is_available}")
                return self.is_available
        except Exception as e:
            logger.error(f"Error conectando con modelo: {e}")
            self.is_available = False
        return False
    
    def analizar_texto(self, texto: str) -> Dict[str, Any]:
        try:
            response = requests.post(
                f"{self.base_url}/predict",
                json={"texto": texto},
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            if data["status"] == "error":
                raise Exception(data.get("error", "Error desconocido"))
            
            return data["resultado"]
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error en petición al modelo: {e}")
            raise Exception(f"No se pudo conectar con el modelo: {str(e)}")
        except Exception as e:
            logger.error(f"Error analizando texto: {e}")
            raise