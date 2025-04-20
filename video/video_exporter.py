from manim import config
from animation.text_animator import TextAnimator

class VideoExporter:
    def __init__(self, srt_file, font_size, output_file='output_video.mp4'):
        self.srt_file = srt_file
        self.font_size = font_size
        self.output_file = output_file
        config.output_file = output_file
        config.format = 'mp4'

    def export(self):
        """
        Exporta o vídeo usando a cena TextAnimator.
        """
        scene = TextAnimator(srt_file=self.srt_file, font_size=self.font_size)
        scene.render()