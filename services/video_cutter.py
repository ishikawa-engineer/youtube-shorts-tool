import os
import datetime
import logging
from moviepy.video.io.VideoFileClip import VideoFileClip


class VideoCutter:

    def cut(self, video_path, start, end, output_dir):

        try:

            logging.info("動画切り抜き処理開始")

            # 出力フォルダ作成
            os.makedirs(output_dir, exist_ok=True)

            # ファイル名生成
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(output_dir, f"short_{timestamp}.mp4")

            # 動画読み込み
            clip = VideoFileClip(video_path)

            # 動画長さチェック
            if end > clip.duration:
                raise Exception("終了時間が動画の長さを超えています")

            # 切り抜き
            subclip = clip.subclip(start, end)

            # 保存
            subclip.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac"
            )

            clip.close()

            logging.info(f"動画切り抜き完了: {output_path}")

            return output_path

        except Exception as e:

            logging.exception("動画切り抜きエラー")
            raise e