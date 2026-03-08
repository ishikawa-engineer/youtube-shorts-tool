import yt_dlp
import logging


class YoutubeDownloader:

    def download(self, url, output_file):

        logging.info("YouTubeダウンロード開始")

        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "outtmpl": output_file,
            "merge_output_format": "mp4",
            "overwrites": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        logging.info("YouTubeダウンロード完了")

        return output_file