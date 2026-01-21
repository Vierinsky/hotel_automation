from pathlib import Path
from datetime import datetime
import shutil
import pandas as pd

def save_output(df: pd.DataFrame, output_dir: Path) -> Path:
    """
    Guarda el DataFrame procesado como archivo de salida.

    El nombre del archivo incluye la fecha para facilitar
    la trazabilidad diaria.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame final listo para ser compartido.
    output_dir : Path
        Directorio donde se guardará el archivo.

    Returns
    -------
    Path
        Ruta del archivo generado.
    """
    # Crea el directorio de salida si no existe
    # parents=True permite crear carpetas intermedias
    # exist_ok=True evita error si ya existe
    output_dir.mkdir(parents=True, exist_ok=True)

    # Obtiene la fecha actual en formato YYYY-MM-DD
    # Se usa para versionar el output por día
    date_str = datetime.now().strftime("%Y-%m-%d")

    # Construye la ruta completa del archivo de salida
    # Ejemplo: opera_clean_2026-01-21.xlsx
    output_path = output_dir / f"opera_clean_{date_str}.xlsx"

    # Escribe el DataFrame a un archivo Excel
    # index=False evita que se escriba el índice del DataFrame
    df.to_excel(output_path, index=False)

    # Devuelve la ruta del archivo generado
    return output_path

def archive_file(file_path: Path, archive_dir:Path) -> Path:
    """
    Mueve un archivo procesado al directorio de archivo (archive).

    Esto evita reprocesar el mismo archivo en ejecuciones futuras.

    Parameters
    ----------
    file_path : Path
        Ruta del archivo original.
    archive_dir : Path
        Directorio donde se archivará el archivo.

    Returns
    -------
    Path
        Nueva ruta del archivo archivado.
    """
    # Crea el directorio de archivo si no existe
    archive_dir.mkdir(parents=True, exist_ok=True)

    # Define la ruta destino manteniendo el nombre original del archivo
    destination = archive_dir / file_path.name

    # Mueve físicamente el archivo desde su ubicación original
    # Se convierte Path a str porque shutil.move trabaja con strings
    shutil.move(str(file_path), str(destination))

    # Devuelve la nueva ubicación del archivo
    return destination