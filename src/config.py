from dataclasses import dataclass
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)

class Settings:
    """
    Contenedor inmutable de configuración del proyecto.

    Agrupa todas las rutas y parámetros necesarios para
    ejecutar el pipeline de automatización.

    Attributes
    ----------
    input_dir : Path
        Directorio donde se encuentran los archivos de entrada (raw).
    archive_dir : Path
        Directorio donde se mueven los archivos ya procesados.
    output_dir : Path
        Directorio donde se generan los archivos de salida.
    log_dir : Path
        Directorio donde se guardan los logs de ejecución.
    opera_pattern : str
        Patrón de nombre para identificar archivos de Opera.
    """

    input_dir: Path
    archive_dir: Path
    output_dir: Path
    log_dir: Path
    opera_pattern: str

def get_settings() -> Settings:
    """
    Carga la configuración del proyecto desde variables de entorno.

    Lee las variables definidas en el archivo `.env` y construye
    un objeto `Settings` con rutas y parámetros tipados.

    Returns
    -------
    Settings
        Objeto de configuración listo para ser usado por el pipeline.

    Raises
    ------
    KeyError
        Si alguna variable de entorno obligatoria no está definida.
    """
    return Settings(
        input_dir=Path(os.environ["INPUT_DIR"]),
        archive_dir=Path(os.environ["ARCHIVE_DIR"]),
        output_dir=Path(os.environ["OUTPUT_DIR"]),
        log_dir=Path(os.environ["LOG_DIR"]),
        opera_pattern=os.environ.get("OPERA_PATTERN", "opera_export_*.csv")
    )