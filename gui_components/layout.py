import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, simpledialog, messagebox
import json

from core.system import system_summary
from core.processes import process_check
from core.network import network_summary
from core.online_intel import online_checks
from core.hibp import check_password_pwned
from core.risk_engine import calculate_risk


class VaultCheckApp:
    def __init__(self, master):
        self.master = master
        master.title("The Intelligence Vault — v2 GUI")
        master.geometry("1000x700")

        # =============================
        # Main container
        # =============================
        main_frame = tk.Frame(master)
        main_frame.pack(expand=True, fill="both")

        # =============================
        # LEFT: Control buttons
        # =============================
        self.button_frame = tk.Frame(main_frame, width=200)
        self.button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        tk.Button(
            self.button_frame,
            text="Run Scan",
            width=20,
            command=self.run_and_render
        ).pack(pady=5)

        tk.Button(
            self.button_frame,
            text="Export JSON",
            width=20,
            command=self.export_json
        ).pack(pady=5)

        tk.Button(
            self.button_frame,
            text="Check Password (HIBP)",
            width=20,
            command=self.check_hibp
        ).pack(pady=5)

        self.online_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            self.button_frame,
            text="Enable Online Checks",
            variable=self.online_var
        ).pack(pady=10)

        # =============================
        # CENTER: Result tabs
        # =============================
        self.tab_control = ttk.Notebook(main_frame)
        self.tab_control.pack(side=tk.LEFT, expand=True, fill="both", padx=5, pady=5)

        self.system_tab = ttk.Frame(self.tab_control)
        self.process_tab = ttk.Frame(self.tab_control)
        self.network_tab = ttk.Frame(self.tab_control)
        self.online_tab = ttk.Frame(self.tab_control)
        self.risk_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.system_tab, text="System")
        self.tab_control.add(self.process_tab, text="Processes")
        self.tab_control.add(self.network_tab, text="Network")
        self.tab_control.add(self.online_tab, text="Online")
        self.tab_control.add(self.risk_tab, text="Risk")

        # =============================
        # RIGHT: Advanced scanning panel
        # =============================
        self.advanced_frame = tk.Frame(main_frame, width=220)
        self.advanced_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

        tk.Label(
            self.advanced_frame,
            text="Advanced Scanning",
            font=("Helvetica", 10, "bold")
        ).pack(anchor="w", pady=(0, 5))

        self.adv_malware = tk.BooleanVar()
        self.adv_rootkit = tk.BooleanVar()
        self.adv_memory = tk.BooleanVar()
        self.adv_behavior = tk.BooleanVar()

        tk.Checkbutton(
            self.advanced_frame,
            text="Deep Malware Scanning",
            variable=self.adv_malware
        ).pack(anchor="w")

        tk.Checkbutton(
            self.advanced_frame,
            text="Rootkit / Backdoor Detection",
            variable=self.adv_rootkit
        ).pack(anchor="w")

        tk.Checkbutton(
            self.advanced_frame,
            text="Memory Analysis",
            variable=self.adv_memory
        ).pack(anchor="w")

        tk.Checkbutton(
            self.advanced_frame,
            text="Behavioral Anomaly Detection",
            variable=self.adv_behavior
        ).pack(anchor="w")

        # =============================
        # State
        # =============================
        self.results = {}

    # ======================================================
    # Core execution
    # ======================================================
    def run_and_render(self):
        self.results = self.run_checks()
        self.render_results()

    def run_checks(self) -> dict:
        results = {
            "system": system_summary(),
            "processes": process_check(),
            "network": network_summary(),
        }

        if self.online_var.get():
            results["online"] = online_checks()
        else:
            results["online"] = {
                "public_ip": "Offline",
                "reputation": "Skipped",
                "source": "Disabled by user"
            }

        results["risk_level"], results["recommendations"] = calculate_risk(results)
        return results

    # ======================================================
    # Rendering
    # ======================================================
    def render_results(self):
        self._render_tab(self.system_tab, self.results.get("system", {}))
        self._render_tab(
            self.process_tab,
            {"Suspicious Processes": self.results.get("processes", {}).get("suspicious_processes", [])}
        )
        self._render_tab(self.network_tab, self.results.get("network", {}))
        self._render_tab(self.online_tab, self.results.get("online", {}))
        self._render_risk_tab()

    def _render_risk_tab(self):
        for widget in self.risk_tab.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.risk_tab)
        frame.pack(expand=True, fill="both", padx=10, pady=10)

        level = self.results.get("risk_level", "UNKNOWN")
        color = {"LOW": "green", "MODERATE": "orange", "ELEVATED": "red"}.get(level, "black")

        tk.Label(
            frame,
            text=f"Overall Risk Level: {level}",
            font=("Arial", 16, "bold"),
            fg=color
        ).pack(pady=10)

        text = scrolledtext.ScrolledText(frame, wrap=tk.WORD)
        text.insert(tk.END, "Recommendations:\n")
        for rec in self.results.get("recommendations", []):
            text.insert(tk.END, f"- {rec}\n")

        text.config(state=tk.DISABLED)
        text.pack(expand=True, fill="both")

    def _render_tab(self, tab, data: dict):
        for widget in tab.winfo_children():
            widget.destroy()

        st = scrolledtext.ScrolledText(tab, wrap=tk.WORD)
        if not data:
            st.insert(tk.END, "No data available.\n")
        else:
            for k, v in data.items():
                if isinstance(v, list):
                    st.insert(tk.END, f"{k}:\n")
                    for item in v:
                        st.insert(tk.END, f"- {item}\n")
                else:
                    st.insert(tk.END, f"{k}: {v}\n")

        st.config(state=tk.DISABLED)
        st.pack(expand=True, fill="both", padx=10, pady=10)

    # ======================================================
    # Utilities
    # ======================================================
    def export_json(self):
        if not self.results:
            messagebox.showwarning("Export JSON", "No results to export.")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        if path:
            with open(path, "w") as f:
                json.dump(self.results, f, indent=2)
            messagebox.showinfo("Export JSON", "Results exported successfully.")

    def check_hibp(self):
        password = simpledialog.askstring(
            "HIBP Check",
            "Enter password to check:",
            show="*"
        )
        if not password:
            return

        count = check_password_pwned(password)

        # Ensure online container exists
        self.results.setdefault("online", {})

        if count is None:
            self.results["online"]["hibp_password_check"] = "Unable to retrieve results"
            messagebox.showinfo("HIBP", "Unable to retrieve results.")

        elif count == 0:
            self.results["online"]["hibp_password_check"] = "Password not found in breaches"
            messagebox.showinfo("HIBP", "Password not found in breaches.")

        else:
            self.results["online"]["hibp_password_check"] = f"Found {count} times"
            messagebox.showwarning(
                "HIBP",
                f"Password found in breaches {count} times!"
            )

        self._render_tab(self.online_tab, self.results.get("online", {}))
