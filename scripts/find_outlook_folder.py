import win32com.client

def walk_folders(folder, prefix=""):
    # Recorre subcarpetas de forma recursiva
    for sub in folder.Folders:
        path = f"{prefix}/{sub.Name}" if prefix else sub.Name
        yield path, sub
        yield from walk_folders(sub, path)

def main():
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

    needle = input("Escriba un texto a buscar (ej: opera): ").strip().lower()
    if not needle:
        print("Debes ingresar un texto.")
        return

    print("\n=== Stores (raíces) disponibles ===")
    roots = list(outlook.Folders)
    for r in roots:
        print("-", r.Name)

    print("\n=== Coincidencias ===")
    found = 0
    for root in roots:
        root_name = root.Name
        # Incluye también la raíz como punto de partida
        for path, _sub in walk_folders(root, prefix=root_name):
            if needle in path.lower():
                print(path)
                found += 1

    if found == 0:
        print("No encontré carpetas que coincidan con ese texto.")

if __name__ == "__main__":
    main()
