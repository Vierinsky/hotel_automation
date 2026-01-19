from pathlib import Path
import pandas as pd

def find_latest_file(input_dir: Path, pattern: str) -> Path | None:
    files = sorted(input_dir.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0] if files else None

def read_export(path: Path) -> pd.DataFrame:
    # asume CSV; Si fuera Excel, usar pd.read_excel
    return pd.read_csv(path, encoding="utf-8", sep=",")
