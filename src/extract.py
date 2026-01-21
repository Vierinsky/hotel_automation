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
    files = sorted(input_dir.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
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
