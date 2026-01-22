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


def split_name(df:pd.DataFrame) -> pd.DataFrame:

    # Espera formatp: "Apellido, Nombre"
    df = df.copy()
    
    # Asegura string y limpia espacios dobles
    df["name"] = df["name"].astype(str).str.strip()
    df["name"] = df["name"].str.replace(r"\s+", " ", regex=True)

    # Separa por la primera coma
    parts = df["name"].str.split(",", n=1, expand=True)

    # Si no hay coma, parts[1] será NaN
    df["last_name"] = parts[0].str.strip()
    df["first_name"] = parts[1].str.strip() if parts.shape[1] > 1 else None

    return df


def build_customer_key_name(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    # Normaliza: minúsculas + sin espacios raros
    ln = df["last_name"].fillna("").str.lower().str.strip()
    fn = df["first_name"].fillna("").str.lower().str.strip()

    # Key simple (En producción considerar hashear)
    df["customer_key_name"] = (ln + "|" + fn).str.replace(r"\s+", " ", regex=True)

    # "Confianza" baja porque solo es nombre
    df["customer_key_confidence"] = "low"

    return df

# =============== MODIFICAR ====================
# En un futuro habría que lidiar con deduplicación de clientes. 
    # Para esto hay que lidiar con el problema de falta de ID único por cliente. 
# También hay que averiguar donde se guarda la info personal de cada cliente. 

# Una solución es implementar una solución temporal por fuera de Opera (Ej. Planilla propia) que cree un "client_id" 

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
    df = df.dropna(subset=["confirmation_number", "arrival_date", "name"])   # TODO: MODIFICAR cuando corresponda

    # Devuelve el DataFrame limpio
    return df