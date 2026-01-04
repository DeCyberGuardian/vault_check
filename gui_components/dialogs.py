import tkinter as tk
from tkinter import simpledialog, messagebox


def confirm_online_checks(parent) -> bool:
    return messagebox.askyesno(
        "Online Intelligence",
        "Online checks will query public services.\n"
        "No personal data is stored or shared.\n\nProceed?",
        parent=parent
    )


def prompt_password(parent) -> str | None:
    return simpledialog.askstring(
        "HIBP Password Check",
        "Enter password to check (input hidden):",
        show="*",
        parent=parent
    )
