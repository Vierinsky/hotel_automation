import pandas as pd
import re

# La siguiente variable es un set y su nombre está en mayuscula ya que esta variable es una constante, por lo tanto, no debería mutar nunca.
REQUIRED_COLUMNS  = {
    "property",             # Propiedad del hotel (ALMASPDV = Stgo, ALMASPUQ = Pta. Arenas, ALMASPUQX = Pta. Arenas Express)
    "confirmation_number",  # String o Int (Ej. 333568932)
    "rate",                 # FLOAT
    # "balance",
    "name",                 # String (Apellido, Nombre)
    # "room",
    "room_type",
    "arrival",              # DATE
    # "nights",
    "departure",            # DATE
    "reservation_type",
    "rate_code",            # "Rate Code" son siglas genéricas de las tarifas. Dato importante: Si la sigla contiene "SD" al final, significa "sin desayuno" 
    "room_type_to_charge",
    "travel_agent"          # Esta columna dice a que OTA corresponde la reserva
}

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza los nombres de columnas del DataFrame.

    - Convierte a minúsculas
    - Elimina espacios iniciales y finales
    - Reemplaza espacios múltiples por uno
    - Reemplaza espacios por '_'

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    pd.DataFrame
    """
    # Crea una copia del DataFrame para no modificar el original
    # Esto evita efectos secundarios en otros pasos del pipeline
    df = df.copy()

    # Normaliza cada nombre de columna:
    # - strip(): elimina espacios al inicio y al final
    # - lower(): convierte a minúsculas
    # - re.sub(): reemplaza uno o más espacios por "_"
    df.columns = [
        re.sub(r"\s+", "_", c.strip().lower())
        for c in df.columns
    ]

    # Devuelve el DataFrame con columnas normalizadas
    return df


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
    # Calcula la diferencia entre las columnas requeridas
    # y las columnas presentes en el DataFrame
    missing = REQUIRED_COLUMNS - set(df.columns)

    # Si el conjunto no está vacío, hay columnas faltantes
    if missing:
        raise ValueError(
            f"Faltan columnas requeridas: {sorted(missing)}"
        )

# =============== MODIFICAR ====================
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
    # Crea una copia del DataFrame para trabajar de forma segura
    df = df.copy()

    # Convierte la columna 'rate' a tipo numérico
    # errors="coerce" convierte valores inválidos en NaN
    df["rate"] = pd.to_numeric(df["rate"], errors="coerce")

    # Elimina filas donde falte información crítica
    # (reservación o fecha de llegada)
    df = df.dropna(subset=["reservation_id", "arrival_date"])   # TODO: MODIFICAR

    # Devuelve el DataFrame limpio
    return df