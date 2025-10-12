from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_service_url: str = "http://beto-model:8002"
    app_name: str = "BETO-Finetuned Modismos Service"
    app_version: str = "1.0.0"
    app_description: str = "Servicio para análisis de modismos usando BETO-Finetuned"
    port: int = 8001

    class Config:
        env_file = ".env"


settings = Settings()