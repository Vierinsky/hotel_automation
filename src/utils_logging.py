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
    log_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = log_dir / f"run_{ts}.log"

    logger = logging.getLogger("hotel_automation")
    logger.setLevel(logging.INFO)

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    # Handler a archivo
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setFormatter(fmt)

    # Handler a cosola (útil cuando lo corres a mano)
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)

    logger.handlers.clear()     # evita duplicados si re-ejecutas en misma sesión
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger