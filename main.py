import customtkinter as ctk
from tkinter import filedialog, messagebox
import pandas as pd
import os

# Note: To run this application, you need to install customtkinter.
# You can install it using pip:
# pip install customtkinter

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
        self.geometry("700x400")
        
        # --- Theme ---
        # Options: "system" (default), "dark", "light"
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

        # --- Drop Zones Frame ---
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
        ctk.CTkButton(main_file_frame, text="Parcourir...", command=self._browse_main_file).grid(row=2, column=0, padx=10, pady=(5,10))

        # --- New Data CSV Zone ---
        new_data_frame = ctk.CTkFrame(files_frame)
        new_data_frame.grid(row=0, column=1, padx=(10, 0), pady=10, sticky="nsew")
        new_data_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(new_data_frame, text="Nouveau Fichier de Données", font=ctk.CTkFont(size=13)).grid(row=0, column=0, padx=10, pady=(10,5))
        self.new_data_label = ctk.CTkLabel(new_data_frame, text="Aucun fichier sélectionné", text_color="gray", wraplength=250)
        self.new_data_label.grid(row=1, column=0, padx=10, pady=5)
        ctk.CTkButton(new_data_frame, text="Parcourir...", command=self._browse_new_data_file).grid(row=2, column=0, padx=10, pady=(5,10))

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
        """Opens a file dialog for the main file."""
        filepath = filedialog.askopenfilename(filetypes=[("Fichiers CSV", "*.csv"), ("Tous les fichiers", "*.*")])
        if filepath:
            self.main_file_path = filepath
            filename = os.path.basename(filepath)
            self.main_file_label.configure(text=filename, text_color=ctk.ThemeManager.theme["CTkLabel"]["text_color"])
            self._check_all_files_loaded()

    def _browse_new_data_file(self):
        """Opens a file dialog for the new data file."""
        filepath = filedialog.askopenfilename(filetypes=[("Fichiers CSV", "*.csv"), ("Tous les fichiers", "*.*")])
        if filepath:
            self.new_data_file_path = filepath
            filename = os.path.basename(filepath)
            self.new_data_label.configure(text=filename, text_color=ctk.ThemeManager.theme["CTkLabel"]["text_color"])
            self._check_all_files_loaded()
        
    def _check_all_files_loaded(self):
        """Checks if both files have been loaded and enables the merge button."""
        if self.main_file_path and self.new_data_file_path:
            self.merge_button.configure(state="normal")
            
    def _reset_interface(self):
        """Resets the UI to its initial state after a successful merge."""
        self.main_file_path = None
        self.new_data_file_path = None
        
        self.main_file_label.configure(text="Aucun fichier sélectionné", text_color="gray")
        self.new_data_label.configure(text="Aucun fichier sélectionné", text_color="gray")
        
        self.merge_button.configure(state="disabled")

    def format_new_data(self, df_new_data):
        """
        This is the function where you will add your specific formatting steps.
        
        Args:
            df_new_data (pd.DataFrame): The DataFrame created from the new data CSV.
            
        Returns:
            pd.DataFrame: The formatted DataFrame.
        """
        # --- START: ADD YOUR FORMATTING LOGIC HERE ---
        
        # Example: Rename a column
        # if 'Old Column Name' in df_new_data.columns:
        #     df_new_data = df_new_data.rename(columns={'Old Column Name': 'New Column Name'})
            
        # Example: Convert a column to datetime
        # if 'Date' in df_new_data.columns:
        #     df_new_data['Date'] = pd.to_datetime(df_new_data['Date'])
            
        # Example: Create a new column based on others
        # if 'First Name' in df_new_data.columns and 'Last Name' in df_new_data.columns:
        #     df_new_data['Full Name'] = df_new_data['First Name'] + ' ' + df_new_data['Last Name']

        print("Formatting new data... (placeholder function)")
        
        # --- END: ADD YOUR FORMATTING LOGIC HERE ---
        
        return df_new_data

    def merge_files(self):
        """
        Reads the CSVs, formats the new data, merges them,
        and prompts the user to save the result.
        """
        if not self.main_file_path or not self.new_data_file_path:
            messagebox.showerror("Erreur", "Veuillez sélectionner les deux fichiers.")
            return

        try:
            # Read the CSV files into pandas DataFrames
            print(f"Lecture du fichier principal : {self.main_file_path}")
            df_main = pd.read_csv(self.main_file_path, low_memory=False)
            
            print(f"Lecture des nouvelles données : {self.new_data_file_path}")
            df_new_data = pd.read_csv(self.new_data_file_path, low_memory=False)

            # --- Formatting Step ---
            df_new_data_formatted = self.format_new_data(df_new_data)
            
            # --- Merging Step ---
            df_merged = pd.concat([df_main, df_new_data_formatted], ignore_index=True)

            print("Fichiers fusionnés avec succès.")
            
            # --- Save the merged file ---
            save_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("Fichiers CSV", "*.csv")],
                title="Enregistrer le fichier fusionné sous..."
            )
            
            if save_path:
                df_merged.to_csv(save_path, index=False)
                messagebox.showinfo("Succès", f"Fichier fusionné enregistré sous :\n{save_path}")
                self._reset_interface()

        except Exception as e:
            messagebox.showerror("Une erreur est survenue", str(e))
            print(f"Erreur : {e}")


if __name__ == "__main__":
    app = CsvMergerApp()
    app.mainloop()
