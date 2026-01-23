import os
from pathlib import Path
import win32com.client

# Extensiones permitidas para descargar

ALLOWED_EXT = {".csv", ".xlsx", ".xls"}

def ensure_dir(p: Path) -> None:
    """
    Asegura que un directorio exista.

    Si el directorio no existe, lo crea junto con
    cualquier carpeta padre necesaria.

    Parameters
    ----------
    p : Path
        Ruta del directorio a crear.
    """
    p.mkdir(parents=True, exist_ok=True)


def get_outlook_folder(namespace, path_parts: list[str]):
    """
    Obtiene una carpeta específica de Outlook a partir de su ruta lógica.

    La ruta se define como una lista de nombres de carpetas,
    por ejemplo: ["Inbox", "Opera test"].

    Este helper navega por la jerarquía de carpetas de Outlook
    usando la API COM.

    Parameters
    ----------
    namespace :
        Namespace MAPI de Outlook (obtenido desde GetNamespace("MAPI")).
    path_parts : list[str]
        Ruta lógica de la carpeta en Outlook.

    Returns
    -------
    folder :
        Objeto Folder de Outlook correspondiente a la ruta indicada.

    Raises
    ------
    ValueError
        Si la ruta no comienza en Inbox (limitación intencional del ejemplo).
    """
    
    # 6 corresponde a la carpeta Inbox por defecto
    folder = namespace.GetDefaultFolder(6)

    # Asumimos que siempre partimos desde inbox
    if path_parts[0].lower() != "inbox":
        raise ValueError(
            "Este helper asume Inbox como carpeta raíz. Ajustable si es necesario."
        )
    
    # Navega por las subcarpetas indicadas
    for name in path_parts[1:]:
        folder = folder.Folders[name]

    return folder


def save_attachments_from_folder(folder, output_dir: Path) -> int:
    """
    Guarda los adjuntos permitidos de los correos contenidos
    en una carpeta de Outlook.

    Solo se descargan adjuntos con extensiones definidas
    en ALLOWED_EXT.

    Parameters
    ----------
    folder :
        Carpeta de Outlook desde donde se leerán los correos.
    output_dir : Path
        Directorio local donde se guardarán los adjuntos.

    Returns
    -------
    int
        Número total de adjuntos guardados.
    """

    ensure_dir(output_dir)
    count = 0

    # Obtiene todos los ítems de la carpeta
    items = folder.Items

    # Ordena por fecha de recepción (Más recientes primero)
    items.Sort("[ReceivedTime]", True)

    # se convierte a lista para evitar problemas
    # al modificar correos mientras se itera
    for msg in list(items):

        # 43 = MailItem (descarta reuniones, notificaciones, etc.)
        if msg.Class != 43:
            continue

        attachments = msg.Attachments
        if attachments.Count == 0:
            continue

        saved_any = False

        # Outlook indexa adjuntos desde 1, no desde 0
        for i in range(1, attachments.Count + 1):
            att = attachments.Item(i)
            name = att.Filename
            ext = Path(name).suffix.lower()

            # Ignora adjuntos no permitidos
            if ext not in ALLOWED_EXT:
                continue

            dest = output_dir / name

            # Evita sobrescribir archivos existentes
            if dest.exists():
                dest = output_dir / f"{dest.stem}_dup{dest.suffix}"

            # Guarda el adjunto en disco
            att.SaveAsFile(str(dest))

            count += 1
            saved_any = True

        # Si se guardó al menos un adjunto,
        # se marca el correo como leído
        if saved_any:
            msg.UnRead = False
            msg.Save()
    
    return count

def move_processed_emails(src_folder, dst_folder_name: str):
    """
    Mueve correos procesados desde una carpeta de Outlook
    a otra carpeta (por ejemplo, 'Automations_Processed').

    Se asume que los correos ya procesados están marcados
    como leídos.

    Parameters
    ----------
    src_folder :
        Carpeta origen de Outlook.
    dst_folder_name : str
        Nombre de la carpeta destino (hermana de la carpeta origen).
    """

    # La carpeta destino busca al mismo nivel que la carpeta origen
    dst_folder = src_folder.Parent.Folders[dst_folder_name]

    items = src_folder.Items
    items.Sort("[ReceivedTime]", True)

    for msg in list(items):
        if msg.Class != 43:
            continue

        # Convención: correo leído = ya procesado
        if msg.UnRead is False:
            msg.Move(dst_folder)
