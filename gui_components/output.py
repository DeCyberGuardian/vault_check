import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText


class OutputFrame(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Output", padding=5)

        self._build_output()

    def _build_output(self):
        self.text_area = ScrolledText(
            self,
            wrap=tk.WORD,
            state="disabled"
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)

    def clear(self):
        self.text_area.configure(state="normal")
        self.text_area.delete("1.0", tk.END)
        self.text_area.configure(state="disabled")

    def write(self, text: str):
        self.text_area.configure(state="normal")
        self.text_area.insert(tk.END, text + "\n")
        self.text_area.configure(state="disabled")
