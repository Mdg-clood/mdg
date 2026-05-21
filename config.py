"""
Chargement centralisé de la configuration (variables d'environnement).

Sépare la config du reste du code pour faciliter les tests et la soutenance.
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Paramètres applicatifs lus depuis l'environnement ou un fichier .env."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    openai_api_key: str = Field(default="", validation_alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o-mini", validation_alias="OPENAI_MODEL")
    # Utilisé lorsque OPENAI_API_KEY est en réalité une clé Google (préfixe AIza...).
    # `flash-lite` a souvent un quota gratuit distinct de `gemini-2.0-flash` (erreurs 429 fréquentes sur ce dernier).
    gemini_model: str = Field(default="gemini-2.0-flash-lite", validation_alias="GEMINI_MODEL")
    # Nom affiché dans l'interface et transmis au modèle (ex. AskGL).
    tutor_name: str = Field(default="AskGL", validation_alias="TUTOR_NAME")


@lru_cache
def get_settings() -> Settings:
    """Instance unique des settings (cache pour éviter de relire le disque)."""
    return Settings()
