import os
import json
from dotenv import load_dotenv
from datetime import timedelta
from typing import Any, List, Optional
from functools import lru_cache
from urllib.parse import urlparse

from pydantic import AnyHttpUrl, Field, ValidationError, parse_obj_as, field_validator, PrivateAttr
from pydantic_settings import BaseSettings, SettingsConfigDict

# Google Cloud imports
try:
    from google.cloud import secretmanager, bigquery, storage as gcs, pubsub_v1, logging as cloud_logging
    GCP_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
except ImportError:
    secretmanager = bigquery = gcs = pubsub_v1 = cloud_logging = None
    GCP_PROJECT = None

# Load .env into environment

load_dotenv(encoding="utf-8")


class Settings(BaseSettings):
    """
    Application settings for OneAPIIRS with optional Google Cloud integrations.
    """
    class Config:
        env_file = ".env",
        env_file_encoding = "utf-8"
        env_prefix = "ONEAPIIRS_"
        case_sensitive = True
        extra = "forbid"

    # --- Required environment variables ---
    SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    DATABASE_URL: str

    # --- JWT settings ---
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 1440

    # --- Application settings ---
    APP_ENV: str = "development"
    DEBUG: bool = False
    RELOAD: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1
    WORKER_CLASS: str = "uvicorn.workers.UvicornWorker"

    # --- API metadata ---
    API_PREFIX: str = "/api/v1"
    API_TITLE: str = "OneAPIIRS - APE Project"
    API_DESCRIPTION: str = "API unificadora para integração com sistemas legados do IRS."
    API_VERSION: str = "v1"
    API_DOCS_URL: Optional[str] = "/docs"
    API_REDOC_URL: Optional[str] = "/redoc"
    API_OPENAPI_URL: Optional[str] = "/openapi.json"
    ENABLE_DOCS: bool = True

    # --- CORS ---
    CORS_ORIGINS: List[AnyHttpUrl] = []
    cors_origins_raw: Optional[str] = "ONEAPIIRS_CORS_ORIGINS"

    # --- Logging settings ---
    LOG_LEVEL: str = "info"
    LOG_FORMAT: str = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

    # --- Google Cloud resource settings ---
    BQ_PROJECT: Optional[str] = None
    BQ_DATASET: Optional[str] = None
    BQ_TABLE: Optional[str] = None
    GCS_RAW_BUCKET: Optional[str] = None
    GCP_PROJECT_ID: Optional[str] = None
    PUBSUB_TOPIC: Optional[str] = None
    PUBSUB_SUBSCRIPTION: Optional[str] = None
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = None

    # --- Private attributes for GCP clients (excluded from schema) ---
    _bq_client: Any = PrivateAttr(default=None)
    _gcs_client: Any = PrivateAttr(default=None)
    _raw_bucket: Any = PrivateAttr(default=None)
    _pubsub_publisher: Any = PrivateAttr(default=None)
    _pubsub_topic_path: Any = PrivateAttr(default=None)
    _log_client: Any = PrivateAttr(default=None)

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def _normalize_cors_origins(cls, v: Any) -> List[AnyHttpUrl]:
        # Normalize CSV, JSON-list or wildcard into a list of AnyHttpUrl
        items: List[str] = []
        if not v or (isinstance(v, str) and v.strip() in ("", "*")):
            return []
        if isinstance(v, str):
            text = v.strip()
            if text.startswith("[") and text.endswith("]"):
                try:
                    items = json.loads(text)
                except json.JSONDecodeError:
                    items = [u.strip() for u in text.strip("[]").split(",") if u.strip()]
            else:
                items = [u.strip() for u in text.split(",") if u.strip()]
        elif isinstance(v, list):
            items = v
        else:
            raise ValueError("Formato inválido para CORS_ORIGINS")

        normalized: List[str] = []
        for u in items:
            if isinstance(u, str) and not urlparse(u).scheme:
                u = "http://" + u
            normalized.append(u)
        try:
            return parse_obj_as(List[AnyHttpUrl], normalized)
        except ValidationError as e:
            raise ValueError(f"URLs inválidas em CORS_ORIGINS: {e}")

    @property
    def access_token_expires(self) -> timedelta:
        return timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)

    @property
    def refresh_token_expires(self) -> timedelta:
        return timedelta(minutes=self.REFRESH_TOKEN_EXPIRE_MINUTES)

    def load_secrets_from_gcp(self) -> None:
        """
        Load SECRET_KEY, REFRESH_SECRET_KEY and DATABASE_URL from GCP Secret Manager.
        Requires GOOGLE_CLOUD_PROJECT env var set.
        """
        if secretmanager and GCP_PROJECT:
            client = secretmanager.SecretManagerServiceClient()
            for field_name, secret_id in [
                ("SECRET_KEY", "oneapiirs-secret-key"),
                ("REFRESH_SECRET_KEY", "oneapiirs-refresh-secret-key"),
                ("DATABASE_URL", "oneapiirs-database-url"),
            ]:
                name = f"projects/{GCP_PROJECT}/secrets/{secret_id}/versions/latest"
                response = client.access_secret_version(name=name)
                setattr(self, field_name, response.payload.data.decode("UTF-8"))

    def init_gcp_clients(self) -> None:
        """
        Initialize Google Cloud clients and store in private attributes.
        """
        # Cloud Logging
        if cloud_logging and GCP_PROJECT:
            self._log_client = cloud_logging.Client()
            self._log_client.setup_logging(log_level=self.LOG_LEVEL.upper())
        # BigQuery
        if bigquery and (self.BQ_PROJECT or GCP_PROJECT):
            proj = self.BQ_PROJECT or GCP_PROJECT
            self._bq_client = bigquery.Client(project=proj)
        # Cloud Storage
        if gcs and self.GCS_RAW_BUCKET:
            proj = self.BQ_PROJECT or GCP_PROJECT
            self._gcs_client = gcs.Client(project=proj)
            self._raw_bucket = self._gcs_client.bucket(self.GCS_RAW_BUCKET)
        # Pub/Sub
        if pubsub_v1 and self.PUBSUB_TOPIC:
            proj = self.BQ_PROJECT or GCP_PROJECT
            self._pubsub_publisher = pubsub_v1.PublisherClient()
            self._pubsub_topic_path = (
                self._pubsub_publisher.topic_path(proj, self.PUBSUB_TOPIC)
            )


@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    settings.load_secrets_from_gcp()
    if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        settings.init_gcp_clients()
    return settings


# Alias for convenience
settings = get_settings()
