from animation.text_animator import TextAnimator
from animation.latex_renderer import LatexRenderer
from animation.subtitle_sync import SubtitleSync
from moviepy.editor import VideoFileClip
import os
import time
from manim import config

class VideoExporter:
    def __init__(self, config):
        self.config = config

    def export(self, text, subtitle_path):
        # Set Manim configuration for output
        config.media_dir = os.path.join(os.getcwd(), "media")
        config.output_file = "TextAnimator"
        config.quality = "high_quality"  # Força 1080p60

        # Synchronize with subtitles (if provided)
        timings = []
        if subtitle_path:
            sync = SubtitleSync(subtitle_path)
            timings = sync.get_timings()

        # Render animation with subtitle timings
        animator = TextAnimator(
            text,
            self.config.font_size,
            self.config.text_color,
            timings=timings,
            is_latex=self.config.is_latex
        )
        animator.render()

        # Wait for rendering to complete
        time.sleep(2)

        # Define the expected video path
        video_path = os.path.join(config.media_dir, "videos", "1080p60", "TextAnimator.mp4")
        print(f"Procurando vídeo em: {video_path}")

        # Verify if the file exists
        if not os.path.exists(video_path):
            video_dir = os.path.join(config.media_dir, "videos", "1080p60")
            if os.path.exists(video_dir):
                print(f"Arquivos no diretório {video_dir}: {os.listdir(video_dir)}")
            raise FileNotFoundError(f"Video file not found at: {video_path}")

        # Export to MP4 using moviepy
        output_path = "output_video.mp4"
        clip = VideoFileClip(video_path)
        clip.write_videofile(output_path, codec="libx264")
        clip.close()