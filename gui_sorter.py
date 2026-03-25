import customtkinter as ctk
import os
from tkinter import filedialog
from sorter_engine import SorterEngine
from sentinel_handler import SentinelController

class TheSorterGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- CONFIGURAZIONE FINESTRA ---
        self.title("THE SORTER v1.0 - [AUTOMATION ENGINE]")
        self.geometry("900x600")
        ctk.set_appearance_mode("dark")
        
        # Inizializzazione Logica
        self.engine = SorterEngine(self.write_log)
        self.sentinel = None
        self.target_path = ""

        # --- LAYOUT ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR (CONTROLLI) ---
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#0a0a0a")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="THE SORTER", font=ctk.CTkFont(family="Impact", size=28, weight="bold"), text_color="#00FF41")
        self.logo_label.pack(pady=20, padx=10)

        self.btn_select = ctk.CTkButton(self.sidebar, text="📂 SELECT FOLDER", fg_color="#1a1a1a", hover_color="#333333", border_width=1, border_color="#00FF41", command=self.select_folder)
        self.btn_select.pack(pady=10, padx=20)

        ctk.CTkLabel(self.sidebar, text="FILTERS", font=("Consolas", 12), text_color="grey").pack(pady=(20,5))
        
        self.sw_media = ctk.CTkSwitch(self.sidebar, text="Images/Video", progress_color="#00FF41")
        self.sw_media.select()
        self.sw_media.pack(pady=5, padx=20, anchor="w")

        self.sw_docs = ctk.CTkSwitch(self.sidebar, text="Documents", progress_color="#00FF41")
        self.sw_docs.select()
        self.sw_docs.pack(pady=5, padx=20, anchor="w")

        self.sw_sentinel = ctk.CTkSwitch(self.sidebar, text="SENTINEL MODE", progress_color="#FF3131", command=self.toggle_sentinel)
        self.sw_sentinel.pack(pady=30, padx=20, anchor="w")

        self.btn_purge = ctk.CTkButton(self.sidebar, text="⚡ PURGE NOW", fg_color="#00FF41", text_color="black", font=("Impact", 18), hover_color="#00CC33", command=self.run_purge)
        self.btn_purge.pack(side="bottom", pady=20, padx=20, fill="x")

        # --- MAIN AREA (TERMINAL) ---
        self.main_frame = ctk.CTkFrame(self, fg_color="#050505")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        self.terminal = ctk.CTkTextbox(self.main_frame, font=("Consolas", 13), fg_color="black", text_color="#00FF41", border_width=1, border_color="#111")
        self.terminal.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.write_log("[SYSTEM] THE SORTER ENGINE READY...")
        self.write_log("[SYSTEM] STILE: CYBER-NEON / SMART-SORTING: ENABLED")

    def write_log(self, message):
        self.terminal.insert("end", f"{message}\n")
        self.terminal.see("end")

    def select_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.target_path = path
            self.write_log(f"[INFO] Cartella selezionata: {path}")

    def run_purge(self):
        if not self.target_path:
            self.write_log("[!] ERRORE: Seleziona prima una cartella!")
            return
        self.engine.purge_folder(self.target_path)

    def toggle_sentinel(self):
        if not self.target_path:
            self.write_log("[!] ERRORE: Seleziona una cartella per attivare la Sentinella!")
            self.sw_sentinel.deselect()
            return

        if self.sw_sentinel.get():
            self.sentinel = SentinelController(self.target_path, self.engine, self.write_log)
            self.sentinel.start()
            self.sw_sentinel.configure(text="SENTINEL: ON")
        else:
            if self.sentinel:
                self.sentinel.stop()
            self.sw_sentinel.configure(text="SENTINEL: OFF")

if __name__ == "__main__":
    app = TheSorterGUI()
    app.mainloop()