import tkinter as tk
from tkinter import ttk


class ControlsFrame(ttk.LabelFrame):
    def __init__(self, parent, on_run, on_export, on_clear):
        super().__init__(parent, text="Controls", padding=10)

        self.on_run = on_run
        self.on_export = on_export
        self.on_clear = on_clear

        self.run_local = tk.BooleanVar(value=True)
        self.enable_online = tk.BooleanVar(value=False)
        self.enable_hibp = tk.BooleanVar(value=False)

        self._build_controls()

    def _build_controls(self):
        ttk.Checkbutton(
            self,
            text="Run local checks",
            variable=self.run_local
        ).pack(anchor="w", pady=2)

        ttk.Checkbutton(
            self,
            text="Enable online intelligence",
            variable=self.enable_online
        ).pack(anchor="w", pady=2)

        ttk.Checkbutton(
            self,
            text="Run HIBP password check",
            variable=self.enable_hibp
        ).pack(anchor="w", pady=2)

        ttk.Separator(self).pack(fill="x", pady=10)

        ttk.Button(
            self,
            text="Run Check",
            command=self.on_run
        ).pack(fill="x", pady=2)

        ttk.Button(
            self,
            text="Export JSON",
            command=self.on_export
        ).pack(fill="x", pady=2)

        ttk.Button(
            self,
            text="Clear Output",
            command=self.on_clear
        ).pack(fill="x", pady=2)
