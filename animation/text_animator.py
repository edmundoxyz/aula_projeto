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
                        # Remover os delimitadores \( \) ou $ $
                        if part.startswith('\\(') and part.endswith('\\)'):
                            part = part[2:-2]
                        elif part.startswith('\\[') and part.endswith('\\]'):
                            part = part[2:-2]
                        elif part.startswith('$') and part.endswith('$'):
                            part = part[1:-1]
                        try:
                            # Envolver a expressão em $...$ para garantir o modo matemático
                            text_part = Tex(f"${part}$", color=subtitle['color'], font_size=font_size)
                        except Exception as e:
                            print(f"Erro ao compilar LaTeX na parte '{part}': {str(e)}")
                            text_part = Text(part, color=subtitle['color'], font_size=font_size)
                    else:
                        # Parte não é matemática, usar Text
                        text_part = Text(part, color=subtitle['color'], font_size=font_size)
                    
                    # Posicionar a parte na linha
                    text_part.align_to([current_x, y_position, 0], LEFT)
                    line_objects.append(text_part)
                    
                    # Atualizar a posição x para a próxima parte
                    current_x += text_part.get_width()
                
                # Agrupar as partes da linha
                line_group = VGroup(*line_objects)
                
                # Ajustar y_position para a próxima linha
                line_height = font_size / 40
                y_position -= line_height
                
                text_objects.extend(line_objects)
            
            # Verificar se o texto ultrapassa a margem inferior
            if y_position < self.margin_bottom:
                # Calcular o deslocamento necessário para que a última linha fique acima da margem inferior
                shift_up = self.margin_bottom - y_position + line_height
                for text in text_objects:
                    text.shift(shift_up * UP)  # Deslocar todas as linhas para cima
            
            # Agrupar todos os objetos de texto
            text_group = VGroup(*text_objects)
            
            # Adicionar animação de texto
            self.play(FadeIn(text_group))
            
            # Animação do cursor para cada linha
            for i, text in enumerate(text_objects):
                cursor.move_to(text.get_left())
                cursor.generate_target()
                cursor.target.move_to(text.get_right())
                # Duração proporcional ao número de objetos de texto
                self.play(MoveToTarget(cursor), run_time=(end_time - start_time) / len(text_objects))
            
            self.play(FadeOut(text_group), FadeOut(cursor))