import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from src.processor import PKTProcessor


class PKTSplitterGUI:

    def __init__(self, root):

        self.root = root

        # ==================================================
        # Fenster
        # ==================================================

        self.root.title("PKT-Aufteilung für Geograf")

        # Startgröße
        self.root.geometry("850x650")

        # Mindestgröße
        self.root.minsize(650, 500)

        # Fenster darf frei vergrößert/verkleinert werden
        self.root.resizable(True, True)

        self.input_file = tk.StringVar()
        self.output_folder = tk.StringVar()

        # ==================================================
        # GUI
        # ==================================================

        self.build_gui()

    # ======================================================
    # GUI aufbauen
    # ======================================================

    def build_gui(self):

        # ==================================================
        # Hauptcontainer
        # ==================================================

        main_frame = ttk.Frame(self.root)

        main_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=15
        )

        # ==================================================
        # Grid-Konfiguration
        # ==================================================

        main_frame.columnconfigure(
            0,
            weight=1
        )

        main_frame.rowconfigure(
            4,
            weight=1
        )

        # ==================================================
        # Kopfbereich
        # ==================================================

        header = ttk.Frame(main_frame)

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 10)
        )

        header.columnconfigure(
            0,
            weight=1
        )

        # ==================================================
        # Trennlinie
        # ==================================================

        separator = ttk.Separator(
            main_frame,
            orient="horizontal"
        )

        separator.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 10)
        )

        # ==================================================
        # Eingabedatei
        # ==================================================

        input_frame = ttk.LabelFrame(
            main_frame,
            text="Eingabedatei"
        )

        input_frame.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(0, 10)
        )

        input_frame.columnconfigure(
            0,
            weight=1
        )

        self.input_entry = ttk.Entry(
            input_frame,
            textvariable=self.input_file
        )

        self.input_entry.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(10, 5),
            pady=10
        )

        ttk.Button(
            input_frame,
            text="Durchsuchen",
            command=self.select_input
        ).grid(
            row=0,
            column=1,
            padx=(5, 10),
            pady=10
        )

        # ==================================================
        # Ausgabeordner
        # ==================================================

        output_frame = ttk.LabelFrame(
            main_frame,
            text="Ausgabeordner"
        )

        output_frame.grid(
            row=3,
            column=0,
            sticky="ew",
            pady=(0, 15)
        )

        output_frame.columnconfigure(
            0,
            weight=1
        )

        self.output_entry = ttk.Entry(
            output_frame,
            textvariable=self.output_folder
        )

        self.output_entry.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(10, 5),
            pady=10
        )

        ttk.Button(
            output_frame,
            text="Durchsuchen",
            command=self.select_output
        ).grid(
            row=0,
            column=1,
            padx=(5, 10),
            pady=10
        )

        # ==================================================
        # Statusbereich
        # ==================================================

        status_frame = ttk.LabelFrame(
            main_frame,
            text="Status"
        )

        status_frame.grid(
            row=4,
            column=0,
            sticky="nsew",
            pady=(0, 10)
        )

        status_frame.columnconfigure(
            0,
            weight=1
        )

        status_frame.rowconfigure(
            0,
            weight=1
        )

        # --------------------------------------------------
        # Textfeld
        # --------------------------------------------------

        self.log = tk.Text(
            status_frame,
            wrap="word",
            font=("Consolas", 10)
        )

        self.log.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(10, 0),
            pady=10
        )

        # --------------------------------------------------
        # Scrollbar
        # --------------------------------------------------

        scrollbar = ttk.Scrollbar(
            status_frame,
            orient="vertical",
            command=self.log.yview
        )

        scrollbar.grid(
            row=0,
            column=1,
            sticky="ns",
            padx=(0, 10),
            pady=10
        )

        self.log.configure(
            yscrollcommand=scrollbar.set
        )

        # ==================================================
        # Button-Bereich
        # ==================================================

        button_frame = ttk.Frame(
            main_frame
        )

        button_frame.grid(
            row=5,
            column=0,
            sticky="ew",
            pady=(0, 5)
        )

        button_frame.columnconfigure(
            0,
            weight=1
        )

        # --------------------------------------------------
        # Verarbeiten Button
        # --------------------------------------------------

        self.process_button = ttk.Button(
            button_frame,
            text="PKT-Datei verarbeiten",
            command=self.process_file
        )

        self.process_button.grid(
            row=0,
            column=0,
            pady=5
        )

        # ==================================================
        # Initialer Status
        # ==================================================

        self.write_log(
            "Bereit. Bitte eine LNE-PKT-Datei auswählen."
        )

    # ======================================================
    # Eingabedatei auswählen
    # ======================================================

    def select_input(self):

        filename = filedialog.askopenfilename(
            title="LNE-PKT-Datei auswählen",
            filetypes=[
                ("PKT-Dateien", "*.PKT"),
                ("Alle Dateien", "*.*")
            ]
        )

        if filename:

            self.input_file.set(filename)

            self.write_log(
                f"Eingabedatei ausgewählt: {filename}"
            )

    # ======================================================
    # Ausgabeordner auswählen
    # ======================================================

    def select_output(self):

        folder = filedialog.askdirectory(
            title="Ausgabeordner auswählen"
        )

        if folder:

            self.output_folder.set(folder)

            self.write_log(
                f"Ausgabeordner ausgewählt: {folder}"
            )

    # ======================================================
    # Status schreiben
    # ======================================================

    def write_log(self, text):

        translated_text = self.translate_log(text)

        self.log.insert(
            "end",
            translated_text + "\n"
        )

        self.log.see("end")

        self.root.update_idletasks()

    # ======================================================
    # Statusmeldungen übersetzen
    # ======================================================

    def translate_log(self, text):

        translations = {

            "Reading PKT...":
                "PKT-Datei wird gelesen...",

            "Applying rules...":
                "Regeln werden angewendet...",

            "Writing LNA...":
                "LNA-Datei wird geschrieben...",

            "Writing Sach...":
                "Sach-Datei wird geschrieben...",

            "Finished.":
                "Verarbeitung abgeschlossen.",
        }

        if text in translations:
            return translations[text]

        if text.startswith("Input File :"):
            return text.replace(
                "Input File :",
                "Eingabedatei:"
            )

        if text.startswith("Output Folder :"):
            return text.replace(
                "Output Folder :",
                "Ausgabeordner:"
            )

        if text.startswith("LNA Output :"):
            return text.replace(
                "LNA Output :",
                "LNA-Ausgabe:"
            )

        if text.startswith("Sach Output:"):
            return text.replace(
                "Sach Output:",
                "Sach-Ausgabe:"
            )

        if text.startswith("Written:"):
            return text.replace(
                "Written:",
                "Gespeichert:"
            )

        return text

    # ======================================================
    # PKT-Datei verarbeiten
    # ======================================================

    def process_file(self):

        # --------------------------------------------------
        # Eingabedatei prüfen
        # --------------------------------------------------

        if self.input_file.get().strip() == "":

            messagebox.showerror(
                "Fehler",
                "Bitte wählen Sie eine Eingabedatei aus."
            )

            return

        # --------------------------------------------------
        # Ausgabeordner prüfen
        # --------------------------------------------------

        if self.output_folder.get().strip() == "":

            messagebox.showerror(
                "Fehler",
                "Bitte wählen Sie einen Ausgabeordner aus."
            )

            return

        # --------------------------------------------------
        # Status löschen
        # --------------------------------------------------

        self.log.delete(
            "1.0",
            "end"
        )

        # --------------------------------------------------
        # Button deaktivieren
        # --------------------------------------------------

        self.process_button.config(
            state="disabled"
        )

        try:

            # ==================================================
            # Prozessor starten
            # ==================================================

            processor = PKTProcessor()

            summary = processor.process(

                input_file=self.input_file.get(),

                output_folder=Path(
                    self.output_folder.get()
                ),

                logger=self.write_log,

                compare_reference=False
            )

            # ==================================================
            # Zusammenfassung
            # ==================================================

            self.write_log("")
            self.write_log(
                "Verarbeitung erfolgreich abgeschlossen."
            )

            self.write_log(
                f"Eingelesene Datensätze: "
                f"{summary['records']}"
            )

            self.write_log(
                f"LNA-Datensätze: "
                f"{summary['lna']}"
            )

            self.write_log(
                f"Sach-Datensätze: "
                f"{summary['sach']}"
            )

            # ==================================================
            # Erfolgsmeldung
            # ==================================================

            messagebox.showinfo(

                "Fertig",

                f"Die Verarbeitung wurde erfolgreich abgeschlossen.\n\n"
                f"Eingelesene Datensätze: {summary['records']}\n"
                f"LNA-Datensätze: {summary['lna']}\n"
                f"Sach-Datensätze: {summary['sach']}\n\n"
                f"Die Dateien wurden im ausgewählten "
                f"Ausgabeordner gespeichert."
            )

        except Exception as e:

            # ==================================================
            # Fehler
            # ==================================================

            self.write_log("")
            self.write_log(
                f"Fehler: {e}"
            )

            messagebox.showerror(
                "Fehler",
                f"Bei der Verarbeitung ist ein Fehler aufgetreten:\n\n"
                f"{e}"
            )

        finally:

            # --------------------------------------------------
            # Button wieder aktivieren
            # --------------------------------------------------

            self.process_button.config(
                state="normal"
            )


# ==========================================================
# Main
# ==========================================================

def main():

    root = tk.Tk()

    app = PKTSplitterGUI(root)

    root.mainloop()


# ==========================================================
# Start
# ==========================================================

if __name__ == "__main__":
    main()