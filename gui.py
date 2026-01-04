import tkinter as tk
from gui_components.layout import VaultCheckApp


def main():
    root = tk.Tk()
    app = VaultCheckApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
