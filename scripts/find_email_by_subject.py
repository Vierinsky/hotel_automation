import win32com.client

def walk_folders(folder, path):
    for sub in folder.Folders:
        new_path = f"{path}/{sub.Name}"
        yield new_path, sub
        yield from walk_folders(sub, new_path)

def safe_str(x):
    try:
        return str(x)
    except Exception:
        return "<unreadable>"

def main():
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    store = outlook.Folders.Item(1)  # store default
    print("Store:", store.Name)

    needle = input("Texto exacto o parcial del Subject: ").strip().lower()
    if not needle:
        print("Debes ingresar un texto.")
        return

    # Busca en TODAS las carpetas del store
    found = 0
    for path, folder in walk_folders(store, store.Name):
        try:
            items = folder.Items
            # Ojo: Items.Count puede ser caro en carpetas enormes; lo dejamos simple.
            for msg in list(items):
                if msg.Class != 43:  # MailItem
                    continue
                subj = safe_str(getattr(msg, "Subject", ""))
                if needle in subj.lower():
                    found += 1
                    print("\nFOUND:")
                    print("Path :", path)
                    print("Subj :", subj)
                    print("Unread:", getattr(msg, "UnRead", None))
                    print("Attachments:", msg.Attachments.Count)
                    # muestra nombres de adjuntos si hay
                    for i in range(1, msg.Attachments.Count + 1):
                        att = msg.Attachments.Item(i)
                        print(" -", att.FileName)
        except Exception:
            continue

    if found == 0:
        print("\nNo encontré ningún correo cuyo Subject contenga:", needle)

if __name__ == "__main__":
    main()
