import os
import time
import urllib.request
import zipfile
import shutil
import logging
import tkinter as tk
from tkinter import ttk, scrolledtext
from github import get_latest_crewlink_exe_url, get_latest_tou_zip_url
from og_install import find_installation
import threading
from tkinter import messagebox

try:
    from rich import print
except ImportError:
    pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("installation.log"), logging.StreamHandler()],
)

tou_zip_path = os.path.join(os.getcwd(), "tou.zip")
crewlink_path = os.path.join(os.getcwd(), "CrewLink.exe")
installation_path = find_installation()
tou_installation_path = os.path.join(
    os.path.dirname(installation_path), "Among Us Mod ToU"
)


class DownloadProgressTracker:
    def __init__(self, description=""):
        self.description = description
        self.last_printed = 0

    def callback(self, count, block_size, total_size):
        current_time = time.time()
        if current_time - self.last_printed >= 1.0:  # Print every second
            percentage = int(count * block_size * 100 / total_size)
            logging.info(f"{self.description} download: {percentage}%")
            self.last_printed = current_time


def check_installation_paths():
    issues = []
    if os.path.exists(tou_installation_path):
        issues.append(
            f"TownOfUs installation folder already exists at: {tou_installation_path}"
        )
    if os.path.exists("temp_extract"):
        issues.append("Temporary extraction folder already exists")
    return issues


class ModInstallerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Amosgus")
        self.root.geometry("600x400")  # Made window larger to accommodate logs

        style = ttk.Style()
        style.configure("AccentButton.TButton", font=("Helvetica", 12, "bold"))

        # Create frame
        self.frame = ttk.Frame(root, padding="20")
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(
            self.frame, text="Amosgus", font=("Helvetica", 14, "bold")
        )
        title_label.pack(pady=10)

        # Checkboxes
        self.tou_var = tk.BooleanVar(value=True)
        self.crewlink_var = tk.BooleanVar(value=True)

        tou_check = ttk.Checkbutton(
            self.frame,
            text="Town of Us",
            variable=self.tou_var,
            state="disabled",
        )
        tou_check.pack(pady=5)

        crewlink_check = ttk.Checkbutton(
            self.frame, text="Better CrewLink", variable=self.crewlink_var
        )
        crewlink_check.pack(pady=5)

        # Add logs display
        self.log_display = scrolledtext.ScrolledText(
            self.frame, width=60, height=10, font=("Consolas", 9), wrap=tk.WORD
        )
        self.log_display.pack(pady=10, fill=tk.BOTH, expand=True)

        # Install button
        self.install_button = ttk.Button(
            self.frame,
            text="Install",
            command=self.install_mods,
            style="AccentButton.TButton",
            padding=10,
        )
        self.install_button.pack(pady=10)

        # Create custom log handler
        self.log_handler = LogTextHandler(self.log_display)
        logging.getLogger().addHandler(self.log_handler)

    def install_mods(self):
        self.install_button.configure(state="disabled")
        # Create installation thread
        install_thread = threading.Thread(target=self.run_installation)
        install_thread.daemon = True
        install_thread.start()

    def run_installation(self):
        try:
            # Run pre-installation checks
            issues = check_installation_paths()
            if issues:
                error_message = "Pre-installation checks failed:\n" + "\n".join(issues)
                self.root.after(0, lambda: self.installation_failed(error_message))
                return

            if self.crewlink_var.get():
                install_crewlink()
            create_tou_folder()
            self.root.after(0, self.installation_complete)
        except Exception as e:
            self.root.after(0, lambda: self.installation_failed(str(e)))

    def installation_complete(self):
        messagebox.showinfo("Success", "Installation completed successfully!")
        self.root.quit()

    def installation_failed(self, error_message):
        messagebox.showerror("Error", f"Installation failed: {error_message}")
        self.install_button.configure(state="normal")


class LogTextHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        self.text_widget.insert(tk.END, msg + "\n")
        self.text_widget.see(tk.END)


def install_crewlink():
    logging.info("Starting CrewLink installation")
    if os.path.exists(crewlink_path):
        logging.info("CrewLink installer already exists, skipping download")
    else:
        url = get_latest_crewlink_exe_url()
        if url is None:
            logging.error("Failed to get latest CrewLink installer URL")
            print("Failed to get latest CrewLink installer URL")
            return

        logging.info(f"Downloading CrewLink from: {url}")
        try:
            progress = DownloadProgressTracker("CrewLink")
            urllib.request.urlretrieve(url, crewlink_path, progress.callback)
            logging.info(f"CrewLink installer downloaded to: {crewlink_path}")
        except Exception as e:
            logging.error(f"Error during CrewLink installation: {str(e)}")
            raise

    try:
        while True:
            try:
                os.startfile(crewlink_path)
                break
            except:
                time.sleep(0.01)
        logging.info("CrewLink installer launched")
    except Exception as e:
        logging.error(f"Error during CrewLink installation: {str(e)}")
        raise


def create_tou_folder():
    logging.info("Starting TownOfUsR installation")

    if os.path.exists(tou_zip_path):
        logging.info("TownOfUsR zip already exists, skipping download")
    else:
        url = get_latest_tou_zip_url()
        logging.info(f"Downloading TownOfUsR from: {url}")
        progress = DownloadProgressTracker("TownOfUsR")
        urllib.request.urlretrieve(url, tou_zip_path, progress.callback)
        logging.info(f"TownOfUsR zip downloaded to: {tou_zip_path}")

    try:
        while not os.path.exists(tou_zip_path):
            time.sleep(0.01)

        logging.info(f"Creating TownOfUsR directory at: {tou_installation_path}")
        shutil.copytree(
            installation_path,
            tou_installation_path,
            dirs_exist_ok=False,
        )
        logging.info("Base game files copied successfully")

        with zipfile.ZipFile(tou_zip_path, "r") as zip_ref:
            logging.info("Extracting TownOfUsR files to temporary directory")
            zip_ref.extractall("temp_extract")

            inner_folder = next(os.walk("temp_extract"))[1][0]
            inner_path = os.path.join("temp_extract", inner_folder)

            for item in os.listdir(inner_path):
                src = os.path.join(inner_path, item)
                dst = os.path.join(tou_installation_path, item)
                if os.path.isdir(src):
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)

            shutil.rmtree("temp_extract")

        logging.info("Opening TownOfUsR folder")
        os.startfile(tou_installation_path)
        logging.info("Installation completed successfully")

    except Exception as e:
        logging.error(f"Error during TownOfUsR installation: {str(e)}")
        raise


if __name__ == "__main__":
    root = tk.Tk()
    app = ModInstallerGUI(root)
    root.mainloop()
