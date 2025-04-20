from manim import Scene, Text, Tex, Circle, Write, WHITE, RIGHT, UP, LEFT, FadeOut, MoveToTarget, AnimationGroup
import re

class TextAnimator(Scene):
    def __init__(self, srt_file, font_size=40):
        self.srt_file = srt_file
        self.default_font_size = font_size  # Tamanho padrão da GUI
        super().__init__()

    def construct(self):
        from .subtitle_sync import parse_srt_with_colors, get_subtitle_timings
        
        # Carregar legendas com cores, LaTeX e tamanho da fonte
        subtitles = parse_srt_with_colors(self.srt_file)
        
        # Definir margens fixas
        left_margin = -6.5  # Margem de 0.5 unidades à esquerda (tela vai de x=-7 a x=7)
        right_margin = 5.0  # Margem de 2 unidades à direita
        top_margin = 3.6  # Margem de 0.4 unidades no topo (tela vai de y=-4 a y=4)
        bottom_margin = -3.6  # Margem inferior simétrica ao topo
        
        # Acumula frases em linhas diferentes
        y_offset = top_margin  # Começa com 0.4 unidades de margem do topo
        text_objects = []  # Lista para armazenar os objetos de texto
        line_spacing = 1.0  # Espaçamento fixo entre linhas
        
        for subtitle in subtitles:
            start_time, end_time = get_subtitle_timings(subtitle['time'])
            duration = end_time - start_time
            
            # Usar tamanho da fonte do .srt ou da GUI
            font_size = subtitle['font_size'] if subtitle['font_size'] is not None else self.default_font_size
            
            # Dividir o texto em linhas usando \n
            lines = subtitle['text'].split('\n')
            
            # Contar linhas não vazias para este subtitle
            valid_lines = [line for line in lines if line.strip()]
            num_lines = len(valid_lines)
            if num_lines == 0:
                continue  # Pula se não houver linhas válidas
            
            # Verifica se o texto atingirá a margem inferior
            lowest_y = y_offset - (num_lines - 1) * line_spacing
            if lowest_y < bottom_margin:
                # Move todos os textos existentes para cima
                shift_amount = (bottom_margin - lowest_y) + line_spacing
                for text_obj in text_objects:
                    text_obj.generate_target()
                    text_obj.target.shift(UP * shift_amount)
                self.play(
                    *[MoveToTarget(text_obj) for text_obj in text_objects],
                    run_time=0.5
                )
                # Ajusta y_offset para todos os textos já renderizados
                y_offset += shift_amount
                print(f"Após rolagem, novo y_offset: {y_offset}")
            
            # Renderizar cada linha na posição correta
            for line in lines:
                line = line.strip()
                if not line:  # Ignorar linhas vazias
                    continue
                
                # Pré-processar a linha para LaTeX
                if subtitle['use_latex']:
                    print(f"Texto LaTeX a ser renderizado: {line}")
                    # Dividir a linha em partes matemáticas e não matemáticas
                    parts = re.split(r'(\\\(.*?\\\)|\\\[.*?\\\]|\$.*?\$)', line)
                    processed_line = ''
                    for part in parts:
                        if not part:
                            continue
                        # Verificar se é uma parte matemática
                        is_math = bool(re.match(r'^\\\(.*?\\\)$|^\\\[.*?\\\]$|^\$.*?\$', part))
                        if is_math:
                            # Remover delimitadores e manter a parte matemática
                            if part.startswith('\\(') and part.endswith('\\)'):
                                part = part[2:-2]
                            elif part.startswith('\\[') and part.endswith('\\]'):
                                part = part[2:-2]
                            elif part.startswith('$') and part.endswith('$'):
                                part = part[1:-1]
                            processed_line += f"${part}$"
                        else:
                            # Parte não matemática: envolver em \text{}
                            # Remover \n ou barras duplas para evitar exibição de código bruto
                            part = part.replace('\\n', '').replace('\\\\', '')
                            processed_line += f"\\text{{{part}}}"
                    
                    try:
                        text_obj = Tex(processed_line, font_size=font_size, color=subtitle['color'])
                    except Exception as e:
                        print(f"Erro ao renderizar LaTeX: {str(e)}")
                        text_obj = Text(line, font_size=font_size, color=subtitle['color'])
                else:
                    # Para texto normal, remover \n ou barras duplas
                    line = line.replace('\\n', '').replace('\\\\', '')
                    text_obj = Text(line, font_size=font_size, color=subtitle['color'])
                
                # Escala o texto ANTES de posicionar
                scale_factor = font_size / 48.0
                text_obj.scale(scale_factor * 2)
                
                # Posiciona o texto alinhado à esquerda, ajustando y
                text_obj.align_to([left_margin, y_offset, 0], LEFT)
                print(f"Renderizando linha na posição y={y_offset}: {line}")
                
                # Sincroniza o cursor com a escrita
                cursor = Circle(radius=0.1, color=WHITE).move_to(text_obj.get_left())
                cursor.generate_target()
                cursor.target.move_to(text_obj.get_right())
                
                try:
                    self.play(
                        AnimationGroup(
                            Write(text_obj, run_time=duration / num_lines),
                            MoveToTarget(cursor, run_time=duration / num_lines)
                        )
                    )
                    self.play(FadeOut(cursor))
                except Exception as e:
                    print(f"Erro durante a animação: {str(e)}")
                    raise
                
                text_objects.append(text_obj)
                y_offset -= line_spacing  # Desce para a próxima linha
            
            self.wait(max(0, duration - 1))
        
        self.wait(2)