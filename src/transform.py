import pandas as pd

# Actualizar según configuración de planillas a transformar

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
    "Room Type to Charge",
    "Travel Agent"          # Esta columna dice a que OTA corresponde la reserva
}

