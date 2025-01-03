import os

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
DOWNLOAD_UPDATE_INTERVAL = 0.5

INSTALLS_DIR = os.path.join(os.getcwd(), "installs")
TOWN_OF_US_ARCHIVE = os.path.join(INSTALLS_DIR, "town_of_us.zip")
CREWLINK_EXECUTABLE = os.path.join(INSTALLS_DIR, "CrewLink.exe")
AUNLOCKER_DLL = os.path.join(INSTALLS_DIR, "AUnlocker.dll")
TEMP_EXTRACT_DIR = "temp_extract"
AMONGUS_MODDED_PATH = os.path.join(os.getcwd(), "game")

os.makedirs(INSTALLS_DIR, exist_ok=True)
