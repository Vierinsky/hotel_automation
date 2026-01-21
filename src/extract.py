from pathlib import Path
import pandas as pd

def find_latest_file(input_dir: Path, pattern: str) -> Path | None:
    """
    Busca el archivo más reciente en un directorio que coincida con un patrón.

    Parameters
    ----------
    input_dir : Path
        Directorio donde buscar archivos.
    pattern : str
        Patrón de búsqueda (ej: 'opera_*.csv').

    Returns
    -------
    Path | None
        Ruta del archivo más reciente encontrado, o None si no hay coincidencias.
    """
    # input_dir.glob(pattern)
    # → devuelve un iterable con todos los archivos que calzan con el patrón
    #   ejemplo: [Path("opera_export_2026-01-20.csv"), Path("opera_export_2026-01-21.csv")]
    
    # sorted(..., key=..., reverse=True)
    # → ordena la lista resultante usando como criterio el tiempo de modificación del archivo
    
    # lambda p: p.stat().st_mtime
    # → para cada archivo (p), obtiene su metadata del sistema
    # → st_mtime = "modification time" (timestamp en segundos)
    # → mientras más grande, más reciente es el archivo

    files = sorted(
        input_dir.glob(pattern),          # lista de archivos que coinciden con el patrón
        key=lambda p: p.stat().st_mtime,   # criterio: fecha de última modificación
        reverse=True                       # orden descendente (más reciente primero)
    )

    # Si la lista no está vacía:
    # - files[0] es el archivo más reciente
    # Si no hay archivos:
    # - devuelve None (para que el caller lo maneje)
    
    return files[0] if files else None

def read_export(path: Path) -> pd.DataFrame:
    """
    Lee un archivo de exportación desde disco y lo carga en un DataFrame.

    Actualmente asume formato CSV, pero puede extenderse a Excel
    u otros formatos según la fuente.

    Parameters
    ----------
    file_path : Path
        Ruta del archivo a leer.

    Returns
    -------
    pd.DataFrame
        DataFrame con los datos del archivo.
    """
    # asume CSV; Si fuera Excel, usar pd.read_excel
    return pd.read_csv(path, encoding="utf-8", sep=",")
