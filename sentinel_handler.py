import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class SentinelHandler(FileSystemEventHandler):
    def __init__(self, target_path, engine, log_callback):
        self.target_path = target_path
        self.engine = engine
        self.log_callback = log_callback
        # Cartella da ignorare per evitare loop infiniti
        self.ignore_dir = os.path.join(target_path, "ORGANIZED")

    def on_created(self, event):
        # Ignora le cartelle, vogliamo solo i file
        if event.is_directory:
            return
        
        # Ignora i file creati dentro la cartella di destinazione (ORGANIZED)
        if self.ignore_dir in event.src_path:
            return

        filename = os.path.basename(event.src_path)
        self.log_callback(f"[SENTINEL] Rilevato nuovo file: {filename}")
        
        # Aspettiamo un secondo per assicurarci che il file sia scritto completamente
        # (Utile per i download o i file copiati)
        time.sleep(1)
        
        # Passiamo il file al motore
        _, ext = os.path.splitext(filename)
        dest_dir = self.engine.get_dest_folder(self.target_path, ext)
        self.engine.safe_move(event.src_path, dest_dir)

class SentinelController:
    def __init__(self, target_path, engine, log_callback):
        self.target_path = target_path
        self.engine = engine
        self.log_callback = log_callback
        self.observer = None

    def start(self):
        event_handler = SentinelHandler(self.target_path, self.engine, self.log_callback)
        self.observer = Observer()
        self.observer.schedule(event_handler, self.target_path, recursive=False)
        self.observer.start()
        self.log_callback(f"[SENTINEL] Modalità SENTINELLA ATTIVA su: {self.target_path}")

    def stop(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.log_callback("[SENTINEL] Modalità SENTINELLA DISATTIVATA.")