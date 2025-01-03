import os
import tkinter
import tkinter.filedialog
import tkinter.messagebox


def _prompt_file():
    """Create a Tk file dialog and cleanup when finished"""
    while True:
        top = tkinter.Tk()
        top.withdraw()  # hide window
        file_name = tkinter.filedialog.askopenfile(
            title="Select Among Us.exe", parent=top
        ).name
        top.destroy()

        amongusfolder = os.path.dirname(file_name)
        amongusdatafolder = os.path.join(amongusfolder, "Among Us_Data")
        amongusexe = os.path.join(amongusfolder, "Among Us.exe")
        is_valid = os.path.exists(amongusexe) and os.path.exists(amongusdatafolder)

        if not is_valid:
            tkinter.messagebox.showerror("Invalid file", "Select Among Us.exe")
            continue

        return str(file_name)


def find_installation():
    """Find the installation folder of Among Us (or prompt it)"""
    possible = [
        # steam
        r"D:\SteamLibrary\steamapps\common\Among Us",
        r"C:\SteamLibrary\steamapps\common\Among Us",
        # egs (non so se esistono)
        r"C:\Program Files\Epic Games\AmongUs",
        r"C:\Program Files\Epic Games\Among Us",
    ]

    for path in possible:
        if os.path.exists(path):
            return path

    return _prompt_file()
