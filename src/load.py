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
    output_dir.mkdir(parents=True, exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d")
    output_path = output_dir / f"opera_clean_{date_str}.xlsx"

    df.to_excel(output_path, index=False)

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
    archive_dir.mkdir(parents=True, exist_ok=True)

    destination = archive_dir / file_path.name
    shutil.move(str(file_path), str(destination))

    return destination