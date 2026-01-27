from dataclasses import dataclass
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

def _parse_bool(value: str, default: bool = False) -> bool:
    """
    Convierte una variable de entorno en un valor booleano.

    Se consideran valores verdaderos:
    - "1", "true", "yes", "y", "on" (case-insensitive)

    Cualquier otro valor devuelve False o el valor por defecto
    si la entrada es None.

    Parameters
    ----------
    value : str | None
        Valor crudo leído desde una variable de entorno.
    default : bool, optional
        Valor a devolver si value es None.

    Returns
    -------
    bool
        Valor booleano interpretado.
    """    
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _parse_outlook_path(value: str) -> list[str]:
    """
    Convierte una ruta lógica de Outlook en una lista de carpetas.

    Ejemplo:
    "Inbox/Opera test" -> ["Inbox", "Opera test"]

    Parameters
    ----------
    value : str
        Ruta lógica definida en .env.

    Returns
    -------
    list[str]
        Lista de nombres de carpetas para navegación en Outlook.
    """
    # Espera "Inbox/Opera test" -> ["Inbox", "Opera test"]
    return [p.strip() for p in value.split("/") if p.strip()]


def _parse_ext_list(value: str) -> set[str]:
    """
    Convierte una lista de extensiones separadas por coma en un set.

    Ejemplo:
    ".csv,.xlsx" -> {".csv", ".xlsx"}

    Parameters
    ----------
    value : str
        String crudo desde la variable de entorno.

    Returns
    -------
    set[str]
        Conjunto de extensiones normalizadas en minúsculas.
    """
    # Espera ".csv,.xlsx" -> {".csv", ".xlsx"}
    parts = [p.strip().lower() for p in value.splits(",") if p.strip()]
    # Asegura que todas tengan punto inicial
    return {p if p.startswith(".") else f".{p}" for p in parts}


@dataclass(frozen=True)

class Settings:
    """
    Contenedor inmutable de configuración del proyecto.

    Este objeto representa la fuente única de verdad para la
    configuración del pipeline y se construye a partir de
    variables de entorno.

    Al ser inmutable (frozen=True), evita modificaciones
    accidentales durante la ejecución del pipeline.

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
    enable_outlook_download : bool
        Indica si la descarga de adjuntos desde Outlook está habilitada.
    outlook_folder_path : list[str]
        Ruta lógica de la carpeta de Outlook a monitorear.
        Ejemplo: ["Inbox", "Opera test"].
    outlook_processed_folder : str | None
        Nombre de la carpeta de Outlook donde se moverán los correos
        procesados. Si es None, no se realiza el movimiento.
    mail_input_dir : Path
        Directorio local donde se guardan los adjuntos descargados
        desde Outlook.
    mail_allowed_ext : set[str]
        Conjunto de extensiones de archivo permitidas para descarga
        desde Outlook.
    """

    input_dir: Path
    archive_dir: Path
    output_dir: Path
    log_dir: Path
    opera_pattern: str

    # integración con Outlook
    enable_outlook_download: bool
    outlook_folder_path: list[str]
    outlook_processed_folder: str | None
    mail_input_dir: Path
    mail_allowed_ext: set[str] 

def get_settings() -> Settings:
    """
    Carga la configuración del proyecto desde variables de entorno.

    Lee las variables definidas en el archivo `.env`, aplica
    normalización y validaciones básicas, y construye un objeto
    `Settings` tipado e inmutable.

    Returns
    -------
    Settings
        Objeto de configuración listo para ser usado por el pipeline.

    Raises
    ------
    KeyError
        Si alguna variable de entorno obligatoria no está definida.
    """
    enable_outlook = _parse_bool(os.environ.get("ENABLE_OUTLOOK_DOWNLOAD", "1"))

    outlook_path_raw = os.environ.get("OUTLOOK_FOLDER_PATH", "Inbox/Opera test")
    outlook_folder_path = _parse_outlook_path(outlook_path_raw)

    outlook_processed = os.environ.get("OUTLOOK_PROCESSED_FOLDER")
    if outlook_processed is not None:
        outlook_processed = outlook_processed.strip() or None

    mail_input_dir = Path(os.environ.get("MAIL_INPUT_DIR", os.environ["INPUT_DIR"]))

    ext_raw = os.environ.get("MAIL_ALLOWED_EXT", ".csv,.xlsx,.xls")
    mail_allowed_ext = _parse_ext_list(ext_raw)

    return Settings(
        input_dir=Path(os.environ["INPUT_DIR"]),
        archive_dir=Path(os.environ["ARCHIVE_DIR"]),
        output_dir=Path(os.environ["OUTPUT_DIR"]),
        log_dir=Path(os.environ["LOG_DIR"]),
        opera_pattern=os.environ.get("OPERA_PATTERN", "opera_export_*.csv"),     # Considerar cambiar patrón de ser necesario.

        enable_outlook_download=enable_outlook,
        outlook_folder_path=outlook_folder_path,
        outlook_processed_folder=outlook_processed,
        mail_input_dir=mail_input_dir,
        mail_allowed_ext=mail_allowed_ext,    
    )