from src.config import get_settings
from src.download_from_outlook import get_outlook_folder
import win32com.client

def main():
    s = get_settings()
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    folder = get_outlook_folder(outlook, s.outlook_folder_path)
    print("OK folder:", folder.Name)

if __name__ == "__main__":
    main()