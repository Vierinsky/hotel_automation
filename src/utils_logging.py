import logging
from pathlib import Path
from datetime import datetime

def setup_logger(log_dir: Path) -> logging.Logger:
    """
    Configura y devuelve un logger para el pipeline.

    El logger escribe:
    - logs persistentes en archivo (uno por ejecución)
    - logs en consola (útil para ejecución manual)

    Parameters
    ----------
    log_dir : Path
        Directorio donde se almacenarán los archivos de log.

    Returns
    -------
    logging.Logger
        Logger configurado y listo para usar.
    """

    # Crea el directorio de logs si no existe
    # parents=True permite crear toda la ruta
    # exist_ok=True evita error si ya existe
    log_dir.mkdir(parents=True, exist_ok=True)

    # Genera un timestamp para nombrar el archivo de log
    # Esto asegura un archivo distinto por ejecución
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = log_dir / f"run_{ts}.log"

    # Obtiene (o crea) un logger con nombre fijo
    # Usar un nombre permite reutilizarlo en otros módulos
    logger = logging.getLogger("hotel_automation")

    # Define el nivel mínimo de severidad que se registrará
    # INFO incluye: INFO, WARNING, ERROR, CRITICAL
    logger.setLevel(logging.INFO)

    # Define el formato común para todos los mensajes de log
    # Incluye fecha/hora, nivel y mensaje
    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    # Handler que escribe los logs en archivo
    # encoding="utf-8" evita problemas con acentos/caracteres especiales
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setFormatter(fmt)

    # Handler que escribe los logs en consola (stdout)
    # Útil cuando ejecutas el script manualmente
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)

    # Limpia handlers existentes para evitar mensajes duplicados
    # Esto es clave si el script se ejecuta más de una vez
    # en la misma sesión de Python
    logger.handlers.clear()

    # Registra ambos handlers en el logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    # Devuelve el logger ya configurado
    return logger