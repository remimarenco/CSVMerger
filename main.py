import customtkinter as ctk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
import os
import csv
from io import StringIO

# Note: To run this application, you need to install customtkinter and numpy.
# You can install them using pip:
# pip install customtkinter numpy

class CsvMergerApp(ctk.CTk):
    """
    A modern GUI application to merge two CSV files using CustomTkinter.
    The user can select the main CSV file and a file with new data.
    The new data is formatted before being appended to the main data.
    """
    def __init__(self):
        super().__init__()

        # --- Window Configuration ---
        self.title("Outil de Fusion CSV")
        self.geometry("700x450")
        
        # --- Theme ---
        ctk.set_appearance_mode("system") 
        ctk.set_default_color_theme("blue")

        self.main_file_path = None
        self.new_data_file_path = None
        
        self._create_widgets()

    def _create_widgets(self):
        """Creates and places the widgets in the main window."""
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Instructions ---
        instruction_label = ctk.CTkLabel(
            self,
            text="Sélectionnez le fichier principal et le fichier de nouvelles données.",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        instruction_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        # --- Files Frame ---
        files_frame = ctk.CTkFrame(self)
        files_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        files_frame.grid_columnconfigure(0, weight=1)
        files_frame.grid_columnconfigure(1, weight=1)

        # --- Main CSV Zone ---
        main_file_frame = ctk.CTkFrame(files_frame)
        main_file_frame.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="nsew")
        main_file_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(main_file_frame, text="Fichier CSV Principal", font=ctk.CTkFont(size=13)).grid(row=0, column=0, padx=10, pady=(10,5))
        self.main_file_label = ctk.CTkLabel(main_file_frame, text="Aucun fichier sélectionné", text_color="gray", wraplength=250)
        self.main_file_label.grid(row=1, column=0, padx=10, pady=5)
        ctk.CTkButton(main_file_frame, text="Parcourir...", command=self._browse_main_file).grid(row=2, column=0, padx=10, pady=(10,10))

        # --- New Data CSV Zone ---
        new_data_frame = ctk.CTkFrame(files_frame)
        new_data_frame.grid(row=0, column=1, padx=(10, 0), pady=10, sticky="nsew")
        new_data_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(new_data_frame, text="Nouveau Fichier de Données", font=ctk.CTkFont(size=13)).grid(row=0, column=0, padx=10, pady=(10,5))
        self.new_data_label = ctk.CTkLabel(new_data_frame, text="Aucun fichier sélectionné", text_color="gray", wraplength=250)
        self.new_data_label.grid(row=1, column=0, padx=10, pady=5)
        ctk.CTkButton(new_data_frame, text="Parcourir...", command=self._browse_new_data_file).grid(row=2, column=0, padx=10, pady=(10,10))

        # --- Merge Button ---
        self.merge_button = ctk.CTkButton(
            self,
            text="Fusionner les Fichiers",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.merge_files,
            state="disabled"
        )
        self.merge_button.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        
    def _browse_main_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Fichiers CSV", "*.csv"), ("Tous les fichiers", "*.*")])
        if filepath:
            self.main_file_path = filepath
            filename = os.path.basename(filepath)
            self.main_file_label.configure(text=filename, text_color=ctk.ThemeManager.theme["CTkLabel"]["text_color"])
            self._check_all_files_loaded()

    def _browse_new_data_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Fichiers CSV", "*.csv"), ("Tous les fichiers", "*.*")])
        if filepath:
            self.new_data_file_path = filepath
            filename = os.path.basename(filepath)
            self.new_data_label.configure(text=filename, text_color=ctk.ThemeManager.theme["CTkLabel"]["text_color"])
            self._check_all_files_loaded()
        
    def _check_all_files_loaded(self):
        if self.main_file_path and self.new_data_file_path:
            self.merge_button.configure(state="normal")
            
    def _reset_interface(self):
        self.main_file_path = None
        self.new_data_file_path = None
        self.main_file_label.configure(text="Aucun fichier sélectionné", text_color="gray")
        self.new_data_label.configure(text="Aucun fichier sélectionné", text_color="gray")
        self.merge_button.configure(state="disabled")

    def format_new_data(self, df_new_data):
        """
        Applique les transformations nécessaires au DataFrame des nouvelles données.
        """
        print("Début du formatage des nouvelles données...")
        
        required_cols = ['Call Time', 'From', 'To', 'Status', 'Talking']
        missing_cols = [col for col in required_cols if col not in df_new_data.columns]
        if missing_cols:
            raise ValueError(f"Colonnes manquantes dans le nouveau fichier : {', '.join(missing_cols)}")

        if df_new_data.empty:
            print("Aucune donnée à formater.")
            return pd.DataFrame()

        # --- Vérification et réorganisation de l'ordre chronologique ---
        #   Conversion explicite de la colonne 'Call Time' et rapport des valeurs
        #   qui ne peuvent pas être converties en datetime.
        original_call_time = df_new_data['Call Time'].copy()
        df_new_data['Call Time'] = pd.to_datetime(original_call_time, errors='coerce')

        # Détecter les conversions rejetées (NaT) pour investiguer les erreurs
        invalid_mask = df_new_data['Call Time'].isna() & original_call_time.notna()
        if invalid_mask.any():
            invalid_values = original_call_time[invalid_mask].unique()
            print(f"[FORMAT_NEW_DATA] ATTENTION : {len(invalid_values)} valeur(s) 'Call Time' non convertibles : {invalid_values}")
            # On peut également écrire ces valeurs dans un fichier log si nécessaire.

        # Supprimer les lignes sans date valide
        df_new_data = df_new_data.dropna(subset=['Call Time']).reset_index(drop=True)

        # S'assurer que l'ordre est du plus ancien au plus récent
        if not df_new_data['Call Time'].is_monotonic_increasing:
            # La colonne n'est pas monotone croissante → on trie explicitement
            print("[FORMAT_NEW_DATA] 'Call Time' n'est pas monotone croissante. Tri croissant explicite…")
            print("Avant tri (top 5) :", df_new_data['Call Time'].head().tolist())
            df_new_data = df_new_data.sort_values('Call Time').reset_index(drop=True)
            print("Après  tri (top 5) :", df_new_data['Call Time'].head().tolist())
        else:
            print("[FORMAT_NEW_DATA] 'Call Time' déjà monotone croissante – aucun tri nécessaire.")

        # Formater les données. La lecture en amont est maintenant propre.
        df_formatted = pd.DataFrame()
        df_formatted['Date'] = df_new_data['Call Time'].dt.strftime('%d/%m/%Y %H:%M:%S')
        df_formatted['Appelant'] = df_new_data['From']
        df_formatted['Destination'] = df_new_data['To']
        df_formatted['Conversation'] = np.where(
            df_new_data['Status'] == 'Unanswered',
            'non répondu',
            df_new_data['Talking']
        )

        # --- Colonnes dérivées supplémentaires ---
        # ID : concaténation de la date formattée et de l'appelant
        df_formatted['ID'] = df_formatted['Date'] + df_formatted['Appelant']

        # Heure : "hhh  -  (hh+1)h" à partir de l'heure de l'appel
        df_formatted['Heure'] = df_new_data['Call Time'].dt.hour.apply(
            lambda h: f"{h:02d}h  - {(h + 1) % 24:02d}h"
        )

        # Répondu : indicateur binaire sur la base de la colonne Conversation
        df_formatted['Répondu'] = np.where(
            df_formatted['Conversation'] == 'non répondu',
            'non répondu',
            'répondu'
        )

        # Durée : secondes totales (minutes*60 + secondes) ou 10000 en cas d'erreur
        duration_td = pd.to_timedelta(df_formatted['Conversation'], errors='coerce')
        df_formatted['Durée'] = (
            duration_td.dt.total_seconds()
            .fillna(10000)
            .astype(int)
        )

        # Mois : clé Année-Mois (YYYY-MM)
        df_formatted['Mois'] = df_new_data['Call Time'].dt.strftime('%Y-%m')
        
        print("Formatage terminé.")
        return df_formatted

    def merge_files(self):
        if not self.main_file_path or not self.new_data_file_path:
            messagebox.showerror("Erreur", "Veuillez sélectionner les deux fichiers.")
            return

        try:
            print(f"Lecture du fichier principal : {self.main_file_path}")
            df_main = pd.read_csv(self.main_file_path, sep=';', low_memory=False)
            
            # --- Robust CSV Reading with pre-processing ---
            print(f"Lecture et pré-traitement des nouvelles données : {self.new_data_file_path}")
            
            with open(self.new_data_file_path, 'r', encoding='utf-8-sig') as f:
                all_lines = f.readlines()
            
            # 1. Get header and data lines, skipping the 'Totals' line
            header_line = all_lines[0].strip().replace('""', '"')
            data_lines = [
                line.strip() for line in all_lines[1:] 
                if line.strip() and not line.strip().startswith('Totals,')
            ]
            
            # 2. Pre-process lines to remove the non-standard wrapping quotes
            cleaned_lines_for_parsing = []
            for line in data_lines:
                # Remove quotes that wrap the entire line, if present
                if line.startswith('"') and line.endswith('"'):
                    line = line[1:-1]
                    # Collapse doubled quotes inside the line so that
                    #   ""No answer, ..."" -> "No answer, ..."
                    line = line.replace('""', '"')
                cleaned_lines_for_parsing.append(line)

            # 3. Use the robust 'csv' module to parse the cleaned lines
            # This correctly handles commas inside properly quoted fields
            header = next(csv.reader([header_line]))
            reader = csv.reader(cleaned_lines_for_parsing)
            data_rows = [row for row in reader if row]
            
            # 4. Create a clean DataFrame
            df_new_data = pd.DataFrame(data_rows, columns=header)
            
            # --- Étape de formatage ---
            df_new_data_formatted = self.format_new_data(df_new_data)
            
            if df_new_data_formatted.empty:
                messagebox.showwarning("Aucune Donnée Valide", "Aucune ligne valide n'a été trouvée dans le fichier de nouvelles données.")
                return

            # --- Étape de fusion ---
            df_merged = pd.concat([df_main, df_new_data_formatted], ignore_index=True)
            print("Fichiers fusionnés avec succès.")
            
            # --- Sauvegarde ---
            save_path = filedialog.asksaveasfilename(
                defaultextension=".csv", filetypes=[("Fichiers CSV", "*.csv")], title="Enregistrer le fichier fusionné sous..."
            )
            
            if save_path:
                df_merged.to_csv(save_path, index=False, sep=';')
                messagebox.showinfo("Succès", f"Fichier fusionné enregistré avec succès sous :\n{save_path}")
                self._reset_interface()

        except Exception as e:
            messagebox.showerror("Une erreur est survenue", str(e))
            print(f"Erreur : {e}")

if __name__ == "__main__":
    app = CsvMergerApp()
    app.mainloop()
