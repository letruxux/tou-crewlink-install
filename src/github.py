import json
import urllib.request


def get_latest_release_assets(author: str, repo: str):
    """example:
    ```py
    [
        {
            "name": "TownOfUs.dll",
            "browser_download_url": "https://github.com/eDonnes124/Town-Of-Us-R/releases/download/v1.0.0/TownOfUs.dll"
        }
    ]
    ```"""
    url = "https://api.github.com/repos/{owner}/{repo}/releases/latest".format(
        owner=author, repo=repo
    )
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode("utf-8"))
    assets = data["assets"]

    return assets


def get_latest_tou_zip_url():
    assets = get_latest_release_assets("eDonnes124", "Town-Of-Us-R")
    for asset in assets:
        if asset["name"].endswith(".zip"):
            return str(asset["browser_download_url"])

    return None


def get_latest_aunlocker_url():
    assets = get_latest_release_assets("astra1dev", "AUnlocker")
    for asset in assets:
        if asset["name"].endswith(".dll"):
            return str(asset["browser_download_url"])

    return None


def get_latest_crewlink_exe_url():
    assets = get_latest_release_assets("OhMyGuus", "BetterCrewLink")
    for asset in assets:
        if asset["name"].endswith(".exe"):
            return str(asset["browser_download_url"])

    return None
