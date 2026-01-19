from dataclasses import dataclass
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    input_dir: Path
    archive_dir: Path
    output_dir: Path
    log_dir: Path
    opera_pattern: str

def get_settings() -> Settings:
    return Settings(
        input_dir=Path(os.environ["INPUT_DIR"]),
        archive_dir=Path(os.environ["ARCHIVE_DIR"]),
        output_dir=Path(os.environ["OUTPUT_DIR"]),
        log_dir=Path(os.environ["LOG_DIR"]),
        opera_pattern=os.environ.get("OPERA_PATTERN", "opera_export_*.csv")
    )