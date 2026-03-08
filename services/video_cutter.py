from moviepy import VideoFileClip
import datetime
import os
import logging


class VideoCutter:

    def cut(self, video_path, start, end, output_dir):

        logging.info("動画切り抜き開始")

        clip = VideoFileClip(video_path).subclipped(start, end)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        filename = f"{output_dir}/cut_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"

        clip.write_videofile(
            filename,
            codec="libx264",
            audio_codec="aac"
        )

        logging.info("動画切り抜き完了")

        return filename