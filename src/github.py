import json
import urllib.request


def get_latest_tou_zip_url():
    url = "https://api.github.com/repos/{owner}/{repo}/releases/latest".format(
        owner="eDonnes124", repo="Town-Of-Us-R"
    )
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode("utf-8"))
    assets = data["assets"]
    for asset in assets:
        if asset["name"].endswith(".zip"):
            return str(asset["browser_download_url"])

    return None


def get_latest_crewlink_exe_url():
    url = "https://api.github.com/repos/{owner}/{repo}/releases/latest".format(
        owner="OhMyGuus", repo="BetterCrewLink"
    )
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode("utf-8"))
    assets = data["assets"]
    for asset in assets:
        if asset["name"].endswith(".exe"):
            return str(asset["browser_download_url"])

    return None
