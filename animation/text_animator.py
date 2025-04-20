from manim import Scene, Text, Tex, FadeIn, FadeOut, Dot, MoveToTarget, WHITE, UP, DOWN, LEFT, VGroup, RIGHT
import re

class TextAnimator(Scene):
    def __init__(self, srt_file, font_size=40):
        self.srt_file = srt_file
        self.default_font_size = font_size  # Tamanho padrão da GUI
        self.margin_top = 3.5  # Margem superior (y = 3.5)
        self.margin_bottom = -3.5  # Margem inferior (y = -3.5)
        self.margin_left = -6.61  # Margem esquerda (x = -6.61)
        self.margin_right = 6.61  # Margem direita (x = 6.61)
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
            
            # Dividir o texto em linhas usando \n
            lines = subtitle['text'].split('\n')
            text_objects = []
            y_position = self.margin_top  # Começar no topo da caixa
            
            # Processar cada linha
            for line in lines:
                line = line.strip()
                if not line:  # Ignorar linhas vazias
                    continue
                
                # Dividir a linha em partes matemáticas e não matemáticas
                parts = re.split(r'(\\\(.*?\\\)|\\\[.*?\\\]|\$.*?\$)', line)
                line_objects = []
                current_x = self.margin_left  # Começar na margem esquerda
                
                for part in parts:
                    part = part.strip()
                    if not part:
                        continue
                    
                    # Verificar se a parte é uma expressão matemática
                    is_math = re.match(r'^\\\(.*?\\\)$|^\\\[.*?\\\]$|^\$.*?\$', part)
                    
                    if subtitle['use_latex'] and is_math:
                        # Parte é uma expressão matemática, usar Tex
                        # Remover os delimitadores \( \) ou $ $ para o Tex
                        if part.startswith('\\(') and part.endswith('\\)'):
                            part = part[2:-2]
                        elif part.startswith('$') and part.endswith('$'):
                            part = part[1:-1]
                        try:
                            text_part = Tex(part, color=subtitle['color'], font_size=font_size)
                        except Exception as e:
                            print(f"Erro ao compilar LaTeX na parte '{part}': {str(e)}")
                            text_part = Text(part, color=subtitle['color'], font_size=font_size)
                    else:
                        # Parte não é matemática, usar Text
                        text_part = Text(part, color=subtitle['color'], font_size=font_size)
                    
                    # Pos