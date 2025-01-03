import os
import shutil
import logging
import urllib.request
import zipfile
from constants import *
from utils import DownloadProgressTracker
from github import (
    get_latest_aunlocker_url,
    get_latest_crewlink_exe_url,
    get_latest_tou_zip_url,
)
from og_install import find_installation
from aunlockerconfig import aunlocker_cfg


def download_file(url: str, destination: str, component_name: str) -> None:
    logging.info(f"Downloading {component_name} from: {url}")
    progress = DownloadProgressTracker(component_name)
    urllib.request.urlretrieve(url, destination, progress.callback)
    logging.info(f"{component_name} downloaded successfully")


def install_crewlink() -> None:
    # check if crewlink is already installed
    if os.path.exists(
        os.path.join(
            os.environ["LOCALAPPDATA"],
            "Programs",
            "bettercrewlink",
            "Better-CrewLink.exe",
        )
    ):
        logging.info("CrewLink is already installed")
        return

    logging.info("Starting CrewLink installation")

    if not os.path.exists(CREWLINK_EXECUTABLE):
        url = get_latest_crewlink_exe_url()
        download_file(url, CREWLINK_EXECUTABLE, "CrewLink")

    os.startfile(CREWLINK_EXECUTABLE)
    logging.info("CrewLink installer launched")


def install_town_of_us() -> None:
    logging.info("Starting Town of Us installation")
    installation_path = find_installation()

    # Download ToU if needed
    if not os.path.exists(TOWN_OF_US_ARCHIVE):
        url = get_latest_tou_zip_url()
        download_file(url, TOWN_OF_US_ARCHIVE, "Town of Us")

    # Setup mod directory
    logging.info(f"Creating mod directory at: {AMONGUS_MODDED_PATH}")
    shutil.copytree(installation_path, AMONGUS_MODDED_PATH, dirs_exist_ok=False)

    # Extract and install files
    with zipfile.ZipFile(TOWN_OF_US_ARCHIVE, "r") as zip_ref:
        zip_ref.extractall(TEMP_EXTRACT_DIR)
        inner_folder = next(os.walk(TEMP_EXTRACT_DIR))[1][0]
        inner_path = os.path.join(TEMP_EXTRACT_DIR, inner_folder)

        for item in os.listdir(inner_path):
            src = os.path.join(inner_path, item)
            dst = os.path.join(AMONGUS_MODDED_PATH, item)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)

        shutil.rmtree(TEMP_EXTRACT_DIR)
    logging.info("Town of Us installation completed successfully")


def install_aunlocker() -> None:
    logging.info("Starting AUnlocker installation")
    if not os.path.exists(AUNLOCKER_DLL):
        url = get_latest_aunlocker_url()
        download_file(url, AUNLOCKER_DLL, "AUnlocker")

        bepinex_dir = os.path.join(AMONGUS_MODDED_PATH, "BepInEx")
        bepinex_plugins = os.path.join(bepinex_dir, "plugins")
        bepinex_cfg = os.path.join(bepinex_dir, "config")
        os.makedirs(bepinex_plugins, exist_ok=True)
        os.makedirs(bepinex_cfg, exist_ok=True)

        shutil.move(AUNLOCKER_DLL, bepinex_plugins)
        logging.info("AUnlocker installed successfully")

        with open(os.path.join(bepinex_cfg, "AUnlocker.cfg"), "w") as f:
            f.write(aunlocker_cfg)

        logging.info("AUnlocker config applied successfully")
