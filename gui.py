import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path

from src.processor import PKTProcessor


class PKTSplitterGUI:

    def __init__(self, root):

        self.root = root

        self.root.title("PKT Splitter for Geograf")
        self.root.geometry("750x550")
        self.root.resizable(False, False)

        self.input_file = tk.StringVar()
        self.output_folder = tk.StringVar()

        self.build_gui()

    def build_gui(self):

        # =======================================
        # Title
        # =======================================

        title = ttk.Label(
            self.root,
            text="PKT Splitter for Geograf",
            font=("Segoe UI", 18, "bold")
        )

        title.pack(pady=20)

        # =======================================
        # Input
        # =======================================

        frame1 = ttk.LabelFrame(
            self.root,
            text="Input File"
        )

        frame1.pack(fill="x", padx=20, pady=10)

        ttk.Entry(
            frame1,
            textvariable=self.input_file,
            width=70
        ).pack(side="left", padx=10, pady=10)

        ttk.Button(
            frame1,
            text="Browse",
            command=self.select_input
        ).pack(side="left", padx=5)

        # =======================================
        # Output
        # =======================================

        frame2 = ttk.LabelFrame(
            self.root,
            text="Output Folder"
        )

        frame2.pack(fill="x", padx=20, pady=10)

        ttk.Entry(
            frame2,
            textvariable=self.output_folder,
            width=70
        ).pack(side="left", padx=10, pady=10)

        ttk.Button(
            frame2,
            text="Browse",
            command=self.select_output
        ).pack(side="left", padx=5)

        # =======================================
        # Process Button
        # =======================================

        ttk.Button(
            self.root,
            text="Process PKT",
            command=self.process_file
        ).pack(pady=20)

        # =======================================
        # Log Window
        # =======================================

        frame3 = ttk.LabelFrame(
            self.root,
            text="Status"
        )

        frame3.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.log = tk.Text(
            frame3,
            height=15
        )

        self.log.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

    # ===========================================

    def select_input(self):

        filename = filedialog.askopenfilename(
            title="Select LNE.PKT",
            filetypes=[
                ("PKT Files", "*.PKT"),
                ("All Files", "*.*")
            ]
        )

        if filename:
            self.input_file.set(filename)

    # ===========================================

    def select_output(self):

        folder = filedialog.askdirectory()

        if folder:
            self.output_folder.set(folder)

    # ===========================================

    def write_log(self, text):

        self.log.insert("end", text + "\n")
        self.log.see("end")

    # ===========================================

    def process_file(self):

        if self.input_file.get() == "":

            messagebox.showerror(
                "Error",
                "Please select an input file."
            )
            return

        if self.output_folder.get() == "":

            messagebox.showerror(
                "Error",
                "Please select an output folder."
            )
            return

        self.log.delete("1.0", "end")

        try:

            processor = PKTProcessor()

            summary = processor.process(

                input_file=self.input_file.get(),

                output_folder=Path(self.output_folder.get()),

                logger=self.write_log,

                compare_reference=False

            )

            self.write_log("")
            self.write_log("Processing completed successfully.")

            messagebox.showinfo(

                "Done",

                f"Records Read : {summary['records']}\n"
                f"LNA Records  : {summary['lna']}\n"
                f"Sach Records : {summary['sach']}"

            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )


def main():

    root = tk.Tk()
    app = PKTSplitterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()