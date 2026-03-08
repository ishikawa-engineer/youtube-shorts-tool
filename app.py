import customtkinter as ctk
import threading
import json
import logging

from services.youtube_downloader import YoutubeDownloader
from services.video_cutter import VideoCutter
from utils.time_utils import get_seconds

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


class ShortsApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("YouTube 動画切り抜きツール")
        self.geometry("650x500")

        with open("config.json") as f:
            self.config = json.load(f)

        self.downloader = YoutubeDownloader()
        self.cutter = VideoCutter()

        self.create_widgets()

    def create_widgets(self):

        self.url_entry = ctk.CTkEntry(self, placeholder_text="YouTube URL", width=550)
        self.url_entry.pack(pady=20)

        start_frame = ctk.CTkFrame(self)
        start_frame.pack(pady=10)

        ctk.CTkLabel(start_frame, text="開始時間").grid(row=0, column=0)

        self.start_h = self.time_entry(start_frame, 1)
        self.start_m = self.time_entry(start_frame, 2)
        self.start_s = self.time_entry(start_frame, 3)

        end_frame = ctk.CTkFrame(self)
        end_frame.pack(pady=10)

        ctk.CTkLabel(end_frame, text="終了時間").grid(row=0, column=0)

        self.end_h = self.time_entry(end_frame, 1)
        self.end_m = self.time_entry(end_frame, 2)
        self.end_s = self.time_entry(end_frame, 3)

        self.progress = ctk.CTkProgressBar(self, width=550)
        self.progress.set(0)
        self.progress.pack(pady=20)

        self.status_label = ctk.CTkLabel(self, text="待機中")
        self.status_label.pack()

        self.run_button = ctk.CTkButton(
            self,
            text="動画を切り抜く",
            command=self.start_process
        )

        self.run_button.pack(pady=30)

    def time_entry(self, parent, col):

        entry = ctk.CTkEntry(parent, width=70)
        entry.grid(row=0, column=col, padx=5)
        entry.insert(0, "0")

        return entry

    def start_process(self):

        thread = threading.Thread(target=self.process)
        thread.start()

    def process(self):

        try:

            url = self.url_entry.get().strip()

            start = get_seconds(
                self.start_h.get(),
                self.start_m.get(),
                self.start_s.get()
            )

            end = get_seconds(
                self.end_h.get(),
                self.end_m.get(),
                self.end_s.get()
            )

            self.update_status("動画ダウンロード中...", 0.3)

            video_path = self.downloader.download(
                url,
                self.config["download_file"]
            )

            self.update_status("動画切り抜き中...", 0.7)

            self.cutter.cut(
                video_path,
                start,
                end,
                self.config["output_dir"]
            )

            self.update_status("完了", 1)

        except Exception as e:

            logging.exception(e)
            self.update_status(f"エラー: {str(e)}", 0)

    def update_status(self, text, progress):

        self.after(0, lambda: self.status_label.configure(text=text))
        self.after(0, lambda: self.progress.set(progress))


if __name__ == "__main__":

    app = ShortsApp()
    app.mainloop()