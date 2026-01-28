import win32com.client

def walk(folder, path):
    for sub in folder.Folders:
        new_path = f"{path}/{sub.Name}"
        yield new_path, sub
        yield from walk(sub, new_path)

def main():
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    needle = "opera test"

    roots = list(outlook.Folders)
    for root in roots:
        root_path = root.Name

        for path, f in walk(root, root_path):
            if needle in path.lower():
                try:
                    items = f.Items
                    count = items.Count
                except Exception:
                    count = "?"
                print(f"{path}  | items={count}")

if __name__ == "__main__":
    main()
