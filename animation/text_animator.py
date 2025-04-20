from manim import Scene, Text, Tex, FadeIn, FadeOut, Dot, MoveToTarget, WHITE, UP, DOWN, LEFT
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
            
            # Dividir o texto em linhas (usando \n no .srt)
            raw_text = subtitle['text']
            # Converter \n para \\ se for modo LaTeX, mas apenas dentro de ambientes matemáticos
            if subtitle['use_latex']:
                # Substituir \n por \\ apenas dentro de \( ... \)
                def replace_newline(match):
                    return match.group(0).replace('\n', '\\\\')
                raw_text = re.sub(r'\\\(.*?\\\)', replace_newline, raw_text, flags=re.DOTALL)
                # Fora do ambiente matemático, \n será tratado como quebra de linha normal
                lines = raw_text.split('\n')
            else:
                lines = raw_text.split('\n')
            
            text_objects = []
            y_position = self.margin_top  # Começar no topo da caixa
            
            # Criar objetos de texto para cada linha
            for line in lines:
                line = line.strip()
                if not line:  # Ignorar linhas vazias
                    continue
                
                # Verificar se a linha contém expressões matemáticas
                has_math = re.search(r'\\\(.*?\\\)', line) is not None
                
                if subtitle['use_latex'] and has_math:
                    # Linha contém matemática, usar Tex
                    try:
                        text = Tex(line, color=subtitle['color'], font_size=font_size)
                    except Exception as e:
                        # Se houver erro no LaTeX, fallback para Text
                        print(f"Erro ao compilar LaTeX na linha '{line}': {str(e)}")
                        text = Text(line, color=subtitle['color'], font_size=font_size)
                else:
                    # Linha não contém matemática ou não está no modo LaTeX, usar Text
                    text = Text(line, color=subtitle['color'], font_size=font_size)
                
                # Alinhar à esquerda e posicionar na margem esquerda
                text.align_to([self.margin_left, y_position, 0], LEFT)
                
                # Ajustar y_position para a próxima linha
                # Estimar a altura da linha (aproximadamente font_size/40 unidades por linha)
                line_height = font_size / 40
                y_position -= line_height  # Mover para baixo para a próxima linha
                
                text_objects.append(text)
            
            # Verificar se o texto ultrapassa a margem inferior
            if y_position < self.margin_bottom:
                # Calcular o deslocamento necessário para que a última linha fique acima da margem inferior
                shift_up = self.margin_bottom - y_position + line_height
                for text in text_objects:
                    text.shift(shift_up * UP)  # Deslocar todas as linhas para cima
            
            # Agrupar todos os objetos de texto
            text_group = self.camera.frame.create_group(*text_objects)
            
            # Adicionar animação de texto
            self.play(FadeIn(text_group))
            
            # Animação do cursor para cada linha
            for i, text in enumerate(text_objects):
                cursor.move_to(text.get_left())
                cursor.generate_target()
                cursor.target.move_to(text.get_right())
                # Duração proporcional ao número de linhas
                self.play(MoveToTarget(cursor), run_time=(end_time - start_time) / len(text_objects))
            
            self.play(FadeOut(text_group), FadeOut(cursor))