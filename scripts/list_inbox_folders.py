import win32com.client

def main():
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6)     # 6 = Inbox

    print("Inbox name:", inbox.Name)
    print("Subcarpetas dentro de Inbox:")
    for f in inbox.Folders:
        print("-", f.Name)

if __name__ == "__main__":
    main()