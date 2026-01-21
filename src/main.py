from src.config import get_settings
from src.utils_logging import setup_logger
from src.extract import find_latest_file, read_export
from src.transform import normalize_columns, validate, basic_clean
from src.load import save_output, archive_file

def main() -> None:
    """
    Punto de entrada principal del pipeline de automatización.

    Orquesta el flujo completo:
    - carga configuración
    - inicializa logging
    - detecta archivo de entrada
    - extrae datos
    - transforma y valida
    - genera output
    - archiva input
    - registra todo en logs
    """
    settings = get_settings()
    logger = setup_logger(settings.log_dir)

    logger.info("Inicio de ejecución del pipeline")

    latest_file = find_latest_file(
        settings.input_dir,
        settings.opera_pattern
    )

    if not latest_file:
        logger.warning("No se encontraron archivos para procesar")
        return
    
    logger.info(f"Archivo detectado: {latest_file.name}")

    df = read_export(latest_file)
    logger.info(f"Filas leídas: {len(df)}")

    df = normalize_columns(df)
    validate(df)
    df = basic_clean(df)

    output_path = save_output(df, settings.output_dir)
    logger.info(f"Output generado: {output_path}")

    archived_path = archive_file(latest_file, settings.archive_dir)
    logger.info(f"Archivo archivado en: {archived_path}")

    logger.info("Ejecución finalizada exitosamente")

if __name__ == "__main__":
    main()
