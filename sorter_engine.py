import os
import shutil
from datetime import datetime

class SorterEngine:
    def __init__(self, log_callback):
        self.log_callback = log_callback
        # Mappa estensioni estesa
        self.extensions = {
            'MEDIA': ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.mp4', '.mkv', '.mov', '.avi', '.heic'],
            'OFFICE': ['.pdf', '.docx', '.xlsx', '.pptx', '.txt', '.csv', '.epub', '.rtf'],
            'ARCHIVES': ['.zip', '.rar', '.7z', '.tar', '.gz'],
            'DEV': ['.py', '.js', '.html', '.css', '.cpp', '.json', '.java', '.php', '.sql'],
            'SETUP': ['.exe', '.msi', '.dmg', '.iso', '.bin']
        }

    def get_dest_folder(self, base_path, file_ext):
        # 1. Trova la categoria
        category = "OTHERS"
        for cat, exts in self.extensions.items():
            if file_ext.lower() in exts:
                category = cat
                break
        
        # 2. Smart Sorting: Anno e Mese
        now = datetime.now()
        year = str(now.year)
        month = now.strftime("%B").capitalize() # Es: Marzo
        
        dest_path = os.path.join(base_path, "ORGANIZED", category, year, month)
        
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
            
        return dest_path

    def safe_move(self, src, dest_dir):
        filename = os.path.basename(src)
        name, ext = os.path.splitext(filename)
        dest = os.path.join(dest_dir, filename)
        
        # Gestione duplicati (evita sovrascrittura)
        counter = 1
        while os.path.exists(dest):
            new_name = f"{name}({counter}){ext}"
            dest = os.path.join(dest_dir, new_name)
            counter += 1
            
        try:
            shutil.move(src, dest)
            self.log_callback(f"[OK] SPOSTATO: {filename} -> {os.path.relpath(dest_dir)}")
            return True
        except Exception as e:
            self.log_callback(f"[ERRORE] Impossibile spostare {filename}: {e}")
            return False

    def purge_folder(self, target_path):
        self.log_callback(f">>> INIZIO PURGE SU: {target_path}")
        files = [f for f in os.listdir(target_path) if os.path.isfile(os.path.join(target_path, f))]
        
        count = 0
        for f in files:
            src_file = os.path.join(target_path, f)
            _, ext = os.path.splitext(f)
            dest_dir = self.get_dest_folder(target_path, ext)
            if self.safe_move(src_file, dest_dir):
                count += 1
        
        self.log_callback(f">>> OPERAZIONE COMPLETATA. FILE ORGANIZZATI: {count}")