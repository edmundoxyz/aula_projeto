from manim import Scene, Text, Tex, FadeIn, FadeOut, Dot, MoveToTarget, WHITE

class TextAnimator(Scene):
    def __init__(self, srt_file, font_size=40):
        self.srt_file = srt_file
        self.default_font_size = font_size  # Tamanho padrão da GUI
        super().__init__()

    def construct(self):
        from .subtitle_sync import parse_srt_with_colors, get_subtitle_timings
        
        # Carregar legendas com cores, LaTeX e tamanho da fonte
        subtitles = parse_srt_with_colors(self.srt_file)
        
        # Cursor para animação
        cursor = Dot(radius=0.1, color=WHITE)
        
        for subtitle in subtitles:
            start_time, end_time = get_subtitle_timings(subtitle['time'])
            
            # Usar tamanho da fonte do .srt ou da GUI
            font_size = subtitle['font_size'] if subtitle['font_size'] is not None else self.default_font_size
            
            # Renderizar texto com LaTeX ou texto normal
            if subtitle['use_latex']:
                text = Tex(subtitle['text'], color=subtitle['color'], font_size=font_size)
            else:
                text = Text(subtitle['text'], color=subtitle['color'], font_size=font_size)
            
            # Adicionar animação de texto
            self.play(FadeIn(text))
            
            # Animação do cursor (simula escrita)
            cursor.move_to(text.get_left())
            cursor.generate_target()
            cursor.target.move_to(text.get_right())
            self.play(MoveToTarget(cursor), run_time=end_time - start_time)
            
            self.play(FadeOut(text), FadeOut(cursor))