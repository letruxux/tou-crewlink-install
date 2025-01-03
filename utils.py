import time
import logging
import tkinter as tk
from typing import Callable

from constants import DOWNLOAD_UPDATE_INTERVAL


class DownloadProgressTracker:
    def __init__(self, description: str = "") -> None:
        self.description = description
        self.last_printed = 0

    def callback(self, count: int, block_size: int, total_size: int) -> None:
        current_time = time.time()
        if current_time - self.last_printed >= DOWNLOAD_UPDATE_INTERVAL:
            percentage = int(count * block_size * 100 / total_size)
            logging.info(f"{self.description} download: {percentage}%")
            self.last_printed = current_time


class LogTextHandler(logging.Handler):
    def __init__(self, text_widget: tk.Text) -> None:
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record: logging.LogRecord) -> None:
        msg = self.format(record)
        self.text_widget.insert(tk.END, msg + "\n")
        self.text_widget.see(tk.END)
