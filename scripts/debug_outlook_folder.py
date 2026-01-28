from pathlib import Path
import win32com.client

def main():
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

    # Ajusta esta ruta si cambias el folder
    path = ["ROOT", "Bandeja de entrada", "Opera test"]

    # Partimos del ROOT store (Item(1) porque COM es 1-based)
    folder = outlook.Folders.Item(1)
    for name in path[1:]:
        # búsqueda case-insensitive
        found = None
        for f in folder.Folders:
            if f.Name.strip().lower() == name.strip().lower():
                found = f
                break
        if not found:
            print(f"No encontré '{name}' dentro de '{folder.Name}'. Subcarpetas disponibles:")
            for f in folder.Folders:
                print("-", f.Name)
            return
        folder = found

    items = folder.Items
    items.Sort("[ReceivedTime]", True)

    print("Carpeta:", folder.Name)
    print("Cantidad de items:", items.Count)
    print("\n--- Últimos 10 correos ---")

    for i, msg in enumerate(list(items)[:10], start=1):
        if msg.Class != 43:
            continue
        subj = msg.Subject
        unread = msg.UnRead
        att_count = msg.Attachments.Count
        print(f"{i}. Unread={unread} | Attachments={att_count} | Subject={subj}")

        # Lista nombres de adjuntos (si hay)
        for j in range(1, att_count + 1):
            att = msg.Attachments.Item(j)
            print(f"   - {att.FileName}")

if __name__ == "__main__":
    main()
