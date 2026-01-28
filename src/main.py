from src.config import get_settings
from src.download_from_outlook import fetch_mail_attachments
from src.utils_logging import setup_logger
from src.extract import find_latest_file, read_export
from src.transform import normalize_columns, validate, basic_clean, split_name, build_customer_key_name
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
    settings = get_settings()                                           # Carga configuración desde .env (rutas, patrones, etc.)
    logger = setup_logger(settings.log_dir)                             # Inicializa logger y define dónde se guardarán los logs

    logger.info("Inicio de ejecución del pipeline")
    
    # descargar adjuntos desde Outlook a carpeta local
    if settings.enable_outlook_download:
        try:
            saved = fetch_mail_attachments(
                outlook_folder_path=settings.outlook_folder_path,
                output_dir=settings.mail_input_dir,
                allowed_ext=settings.mail_allowed_ext,
                processed_folder_name=settings.outlook_processed_folder,
                logger=logger,
            )
            logger.info(f"Adjuntos descargados desde Outlook: {saved}")                     # Marca inicio de ejecución (útil para auditoría y debugging)
        except Exception as e:
            # Para mockup, NO matar todo el pipeline por falla Outlook.
            logger.warning(f"Falla al descargar adjuntos desde Outlook: {e}")
    
    # downloaded = fetch_mail_attachments(
    #     outlook_folder_path=settings.outlook_folder_path,
    #     output_dir=settings.mail_input_dir,
    #     allowed_ext=settings.mail_allowed_ext,
    #     logger=logger
    # )

    # if downloaded:
    #     logger.info(f"Adjuntos descargados desde Outlook: {downloaded}")

    # fetch_mail_attachments(
    #     outlook_folder_path=settings.outlook_folder_path,
    #     output_dir=settings.mail_input_dir,  # O settings.mail_input_dir si lo separamos
    #     allowed_ext=settings.mail_allowed_ext,
    #     processed_folder_name=settings.outlook_processed_folder,
    #     logger=logger
    # )

    # Decide desde qué carpeta leer archivos:
    # - Si Outlook está habilitado → usa carpeta de adjuntos descargados
    # - Si no → usa input_dir tradicional
    effective_input_dir = (
        settings.mail_input_dir
        if settings.enable_outlook_download
        else settings.input_dir
    )

    latest_file = find_latest_file(                                     # Busca el archivo más reciente que calce con el patrón configurado
        settings.input_dir,
        settings.opera_pattern
    )

    if not latest_file:                                                 # Si no hay archivo, se registra y se termina la ejecución
        logger.warning("No se encontraron archivos para procesar")
        return
    
    logger.info(f"Archivo detectado: {latest_file.name}")               # Registra el nombre del archivo detectado

    df = read_export(latest_file)                                       # Lee el archivo de entrada y lo carga en un DataFrame
    logger.info(f"Filas leídas: {len(df)}")

    df = normalize_columns(df)                                          # Normaliza nombres de columnas, valida estructura y limpia datos
    validate(df)
    df = basic_clean(df)

    df = split_name(df)
    df = build_customer_key_name(df)

    output_path = save_output(df, settings.output_dir)                  # Genera el archivo de salida (Excel/CSV limpio)
    logger.info(f"Output generado: {output_path}")

    archived_path = archive_file(latest_file, settings.archive_dir)     # Mueve el archivo original a la carpeta de archivo
    logger.info(f"Archivo archivado en: {archived_path}")

    logger.info("Ejecución finalizada exitosamente")                    # Marca ejecución exitosa

if __name__ == "__main__":                                              # Permite ejecutar este script directamente o como módulo
    main()
