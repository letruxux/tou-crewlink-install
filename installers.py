import os
import shutil
import logging
import urllib.request
import zipfile
from typing import Optional
from constants import *
from utils import DownloadProgressTracker
from github import get_latest_crewlink_exe_url, get_latest_tou_zip_url
from og_install import find_installation


def install_crewlink() -> None:
    logging.info("Starting CrewLink installation")

    if not os.path.exists(CREWLINK_EXECUTABLE):
        url = get_latest_crewlink_exe_url()
        if not url:
            raise RuntimeError("Failed to get latest CrewLink installer URL")

        logging.info(f"Downloading CrewLink from: {url}")
        progress = DownloadProgressTracker("CrewLink")
        urllib.request.urlretrieve(url, CREWLINK_EXECUTABLE, progress.callback)

    os.startfile(CREWLINK_EXECUTABLE)
    logging.info("CrewLink installer launched")


def install_town_of_us() -> None:
    logging.info("Starting Town of Us installation")
    installation_path = find_installation()
    mod_install_path = os.path.join(
        os.path.dirname(installation_path), "Among Us Mod TownOfUs"
    )

    download_mod()
    create_mod_directory(installation_path, mod_install_path)
    extract_and_copy_files(mod_install_path)

    os.startfile(mod_install_path)
    logging.info("Installation completed successfully")


def download_mod() -> None:
    if not os.path.exists(TOWN_OF_US_ARCHIVE):
        url = get_latest_tou_zip_url()
        logging.info(f"Downloading Town of Us from: {url}")
        progress = DownloadProgressTracker("Town of Us")
        urllib.request.urlretrieve(url, TOWN_OF_US_ARCHIVE, progress.callback)


def create_mod_directory(src: str, dst: str) -> None:
    logging.info(f"Creating mod directory at: {dst}")
    shutil.copytree(src, dst, dirs_exist_ok=False)


def extract_and_copy_files(mod_path: str) -> None:
    with zipfile.ZipFile(TOWN_OF_US_ARCHIVE, "r") as zip_ref:
        zip_ref.extractall(TEMP_EXTRACT_DIR)

        inner_folder = next(os.walk(TEMP_EXTRACT_DIR))[1][0]
        inner_path = os.path.join(TEMP_EXTRACT_DIR, inner_folder)

        for item in os.listdir(inner_path):
            src = os.path.join(inner_path, item)
            dst = os.path.join(mod_path, item)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)

        shutil.rmtree(TEMP_EXTRACT_DIR)
