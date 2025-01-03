import logging
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from constants import *
from utils import LogTextHandler
from installers import install_crewlink, install_town_of_us

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("installation.log"), logging.StreamHandler()],
)


class ModInstallerGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.setup_window()
        self.create_widgets()
        self.setup_logging()

    def setup_window(self) -> None:
        self.root.title("Among Us Mod Installer")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        style = ttk.Style()
        style.configure("AccentButton.TButton", font=("Helvetica", 12, "bold"))

    def create_widgets(self) -> None:
        self.frame = ttk.Frame(self.root, padding="20")
        self.frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            self.frame, text="Among Us Mod Installer", font=("Helvetica", 14, "bold")
        ).pack(pady=10)

        self.tou_var = tk.BooleanVar(value=True)
        self.crewlink_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(
            self.frame, text="Town of Us", variable=self.tou_var, state="disabled"
        ).pack(pady=5)
        ttk.Checkbutton(
            self.frame, text="Better CrewLink", variable=self.crewlink_var
        ).pack(pady=5)

        self.log_display = scrolledtext.ScrolledText(
            self.frame, width=60, height=10, font=("Consolas", 9), wrap=tk.WORD
        )
        self.log_display.pack(pady=10, fill=tk.BOTH, expand=True)

        self.install_button = ttk.Button(
            self.frame,
            text="Install",
            command=self.install_mods,
            style="AccentButton.TButton",
            padding=10,
        )
        self.install_button.pack(pady=10)

    def setup_logging(self) -> None:
        self.log_handler = LogTextHandler(self.log_display)
        logging.getLogger().addHandler(self.log_handler)

    def install_mods(self) -> None:
        self.install_button.configure(state="disabled")
        thread = threading.Thread(target=self.run_installation)
        thread.daemon = True
        thread.start()

    def run_installation(self) -> None:
        try:
            if self.crewlink_var.get():
                install_crewlink()
            install_town_of_us()
            self.root.after(0, self.installation_complete)
        except Exception as e:
            self.root.after(0, lambda: self.installation_failed(str(e)))

    def installation_complete(self) -> None:
        messagebox.showinfo(
            "Success", "Installation completed successfully. open Among Us.exe"
        )
        self.root.quit()

    def installation_failed(self, error_message: str) -> None:
        messagebox.showerror("Error", f"Installation failed: {error_message}")
        self.install_button.configure(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    app = ModInstallerGUI(root)
    root.mainloop()
