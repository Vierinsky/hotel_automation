import pandas as pd

# Actualizar según configuración de planillas a transformar

# La siguiente variable es un set y su nombre está en mayuscula ya que esta variable es una constante, por lo tanto, no debería mutar nunca.
REQUIRED_COLUMNS  = {
    "Property",             # Propiedad del hotel (ALMASPDV = Stgo, ALMASPUQ = Pta. Arenas, ALMASPUQX = Pta. Arenas Express)
    "Confirmation Number",  # String o Int (Ej. 333568932)
    "Rate",                 # FLOAT
    # "Balance",
    "Name",                 # String (Apellido, Nombre)
    # "Room",
    "Room Type",
    "Arrival",              # DATE
    # "Nights",
    "Departure",            # DATE
    "Reservation Type",
    "Rate Code",            # "Rate Code" son siglas genéricas de las tarifas. Dato importante: Si la sigla contiene "SD" al final, significa "sin desayuno" 
    # "Room Type to Charge",
    "Travel Agent"          # Esta columna dice a que OTA corresponde la reserva
}

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza los nombres de las columnas del DataFrame.

    - Convierte todos los nombres a minúsculas
    - Elimina espacios al inicio y al final

    Esto permite trabajar de forma consistente aunque
    los archivos de entrada tengan diferencias de formato.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame original leído desde un archivo externo.

    Returns
    -------
    pd.DataFrame
        Copia del DataFrame con nombres de columnas normalizados.
    """
    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]
    return df

# ========== MODIFICAR =============

def validate(df: pd.DataFrame) -> None:
    """
    Valida que el DataFrame contenga todas las columnas requeridas.

    Si falta al menos una columna obligatoria, lanza un ValueError
    con el detalle de las columnas ausentes.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame ya normalizado.

    Raises
    ------
    ValueError
        Si faltan columnas requeridas.
    """
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(
            f"Faltan columnas requeridas: {sorted(missing)}"
        )

# ========== MODIFICAR =============

def basic_clean(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica una limpieza básica de datos al DataFrame.

    - Convierte la columna 'rate' a numérica
    - Elimina filas sin 'reservation_id' o 'arrival_date'

    Esta función asume que el DataFrame ya fue validado.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame validado y con columnas normalizadas.

    Returns
    -------
    pd.DataFrame
        DataFrame limpio, listo para consolidación o carga.
    """
    df = df.copy()

    df["rate"] = pd.to_numeric(df["rate"], errors="coerce")
    df = df.dropna(subset=["reservation_id", "arrival_date"])

    return df