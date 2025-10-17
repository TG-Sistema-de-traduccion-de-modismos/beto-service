# **BETO Service**

**Servicio orquestador para procesamiento de modismos.** 
Este servicio actúa como intermediario entre el orquestador y el modelo BETO, gestionando las peticiones, validando entradas y formateando respuestas.

## **Resumen**
**BETO Service** se encarga de:
- **Recibir** peticiones de los clientes
- **Validar** el formato de entrada
- **Comunicarse** con beto-model
- **Procesar** las respuestas
- **Formatear** y entregar resultados

---

## **Tecnologías principales**
- FastAPI
- Pydantic para validación
- httpx para comunicación asíncrona
- Python 3.10+
- Docker

---

## **Estructura del proyecto**
```
beto-service/
├── Dockerfile
├── requirements.txt
├── .env
└── app/
    ├── main.py              # Punto de entrada FastAPI
    ├── infrastructure/
    │   └── routes.py        # Endpoints HTTP
    ├── application/
    │   └── model_client.py       # Lógica de comunicación con beto-model
    ├── core/
    │   ├── config.py        # Configuración
    │   └── logging_config.py
    └── domain/
        └── models.py        # Modelos Pydantic
        └── vocabulario.py 
```

---

## **Endpoints**

### **GET /health**
Verifica:
- Estado del servicio
- Conectividad con beto-model
- Configuración activa

### **POST /analyze**
Endpoint principal que:
1. Recibe texto a analizar
2. Valida formato y longitud
3. Comunica con beto-model
4. Procesa respuesta
5. Retorna análisis formateado

**Entrada:**
```json
{
    "texto": "Ese camello me tiene exhausto"
}
```

**Respuesta:**
```json
{
    "texto_original": "Ese camello me tiene exhausto",
    "modismos_detectados": {
        "camello": "trabajo"
    },
    "modismos_detallados": [
        {
            "palabra": "camello",
            "significado_detectado": "trabajo",
            "contexto": "Ese camello me tiene exhausto",
            "confianza": 0.982
        }
    ],
    "total_modismos": 1
}
```

---

## **Docker — Build & Run**

1) Construir:
```sh
docker build -t beto-service:latest ./beto-service
```
> **Nota:** la imagen resultante pesa aproximadamente **229.71 MB**.

2) Ejecutar:
```sh
docker run --rm --name beto-service \
    -p 8001:8001 \
    --env-file .env \
    beto-service:latest
```

---

## **Configuración**
- Ajustar variables en `.env` y `config.py` según tu entorno:
  - URLs de servicios
  - Puertos
  - Timeouts
  - Niveles de logging

---

## **Integración y dependencias**
- Requiere acceso a **beto-model**
- Recomendado usar en conjunto con **phi-model**
- Compatible con orquestación via docker-compose

---

## **Notas operativas**
- Servicio stateless
- Optimizado para procesamiento asíncrono
- Incluye circuit breakers para fallos de beto-model
- Logging estructurado para monitoreo
