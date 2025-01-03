import time
import logging
import tkinter as tk
from typing import Callable

from constants import DOWNLOAD_UPDATE_INTERVAL


class DownloadProgressTracker:
    def __init__(self, description: str = "") -> None:
        self.description = description
        self.last_printed = 0
        self.previous_percentage = 0

    def callback(self, count: int, block_size: int, total_size: int) -> None:
        current_time = time.time()
        if current_time - self.last_printed >= DOWNLOAD_UPDATE_INTERVAL:
            percentage = int(count * block_size * 100 / total_size)
            self.last_printed = current_time
            if percentage != self.previous_percentage:
                logging.info(f"{self.description} download: {percentage}%")


class LogTextHandler(logging.Handler):
    def __init__(self, text_widget: tk.Text) -> None:
        super().__init__()
        self.text_widget = text_widget
        self.autoscroll = True
        self.text_widget.bind("<MouseWheel>", self._on_scroll)
        self.text_widget.bind("<Button-4>", self._on_scroll)
        self.text_widget.bind("<Button-5>", self._on_scroll)

    def _on_scroll(self, *args):
        # Disable autoscroll when user manually scrolls up
        current_pos = float(self.text_widget.yview()[1])
        self.autoscroll = current_pos >= 1.0

    def emit(self, record: logging.LogRecord) -> None:
        msg = self.format(record)
        self.text_widget.insert(tk.END, msg + "\n")
        if self.autoscroll:
            self.text_widget.see(tk.END)
