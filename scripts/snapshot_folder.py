import win32com.client

def get_folder(outlook, path):
    folder = outlook.Folders.Item(1)    # store
    for name in path[1:]:
        found = None
        for f in folder.Folders:
            if f.Name.strip().lower() == name.strip().lower():
                found = f
                break
        if not found:
            print("No encontré:", name, "dentro de", folder.Name)
            return None
        folder = found
    return folder

def show(folder, title, n=10):
    items = folder.Items
    items.Sort("[ReceivedTime]", True)
    print(f"\n== {title} ({folder.Name}) ==")
    shown = 0
    for msg in list(items):
        if msg.Class != 43:
            continue
        print(f"- UnRead={msg.UnRead} | Att={msg.Attachments.Count} | {msg.Subject}")
        shown += 1
        if shown >= n:
            break

def main():
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    f1 = get_folder(outlook, ["ROOT", "Bandeja de entrada", "Opera test"])
    f2 = get_folder(outlook, ["ROOT", "Bandeja de entrada", "Processed"])
    if f1: show(f1, "Origen")
    if f2: show(f2, "Procesados")

if __name__ == "__main__":
    main()