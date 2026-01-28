from pathlib import Path
import logging

from src.download_from_outlook import fetch_mail_attachments
from src.config import get_settings
from src.utils_logging import setup_logger

def main():
    s = get_settings()
    logger = setup_logger(s.log_dir)

    saved = fetch_mail_attachments(
        outlook_folder_path=s.outlook_folder_path,
        output_dir=s.mail_input_dir,
        allowed_ext=s.mail_allowed_ext,
        processed_folder_name=s.outlook_processed_folder,
        logger=logger,
    )
    print("Adjuntos guardados:", saved)

if __name__ == "__main__":
    main()
