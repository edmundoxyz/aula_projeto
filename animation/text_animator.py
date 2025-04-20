from manim import Scene, Text, Tex, Circle, Write, WHITE, RIGHT, UP, LEFT, FadeOut, MoveToTarget, AnimationGroup, config
import re

class TextAnimator(Scene):
    def __init__(self, srt_file, font_size=40):
        self.srt_file = srt_file
        self.default_font_size = font_size
        config["disable_caching"] = True
        super().__init__()

    def construct(self):
        from .subtitle_sync import parse_srt_with_colors, get_subtitle_timings
        
        try:
            # Carregar legendas
            subtitles = parse_srt_with_colors(self.srt_file)
            print(f"Total de legendas carregadas: {len(subtitles)}")
            print("Legendas carregadas:", subtitles)
            if not subtitles:
                print("Nenhuma legenda foi carregada. Verifique o arquivo .srt.")
                text_obj = Text("Nenhuma legenda encontrada!", font_size=40, color=WHITE)
                text_obj.move_to([0, 0, 0])
                self.play(Write(text_obj, run_time=2))
                self.wait(2)
                return
        except Exception as e:
            print(f"Erro ao carregar legendas: {str(e)}")
            raise

        # Definir margens fixas
        left_margin = -6.5
        right_margin = 5.0
        top_margin = 3.6
        bottom_margin = -3.6
        
        y_offset = top_margin
        text_objects = []
        line_spacing = 1.0
        
        for subtitle in subtitles:
            try:
                start_time, end_time = get_subtitle_timings(subtitle['time'])
                duration = end_time - start_time
                print(f"Processando subtitle: {subtitle}")
                
                if duration <= 0:
                    print(f"Duração inválida para subtitle {subtitle['number']}: {duration} segundos. Pulando...")
                    continue
                
                font_size = subtitle['font_size'] if subtitle['font_size'] is not None else self.default_font_size
                
                text_content = subtitle.get('text', '')
                if not text_content:
                    print(f"Texto do subtitle está vazio: {subtitle}")
                    continue
                lines = text_content.split('\n')
                print(f"Linhas do subtitle: {lines}")
                
                valid_lines = [line for line in lines if line.strip()]
                num_lines = len(valid_lines)
                print(f"Número de linhas válidas: {num_lines}")
                if num_lines == 0:
                    print("Nenhuma linha válida encontrada neste subtitle. Pulando...")
                    continue
                
                lowest_y = y_offset - (num_lines - 1) * line_spacing
                if lowest_y < bottom_margin:
                    shift_amount = (bottom_margin - lowest_y) + line_spacing
                    for text_obj in text_objects:
                        text_obj.generate_target()
                        text_obj.target.shift(UP * shift_amount)
                    self.play(
                        *[MoveToTarget(text_obj) for text_obj in text_objects],
                        run_time=0.5
                    )
                    y_offset += shift_amount
                    print(f"Após rolagem, novo y_offset: {y_offset}")
                
                # Renderizar cada linha como um objeto separado
                current_y = y_offset
                for line in lines:
                    line = line.strip()
                    if not line:
                        print(f"Linha vazia ignorada: '{line}'")
                        continue
                    
                    print(f"Processando linha: '{line}'")
                    
                    if subtitle.get('use_latex', False):
                        print(f"Texto LaTeX a ser renderizado: {line}")
                        parts = re.split(r'(\\\(.*?\\\)|\\\[.*?\\\]|\$.*?\$)', line)
                        processed_line = ''
                        for part in parts:
                            if not part:
                                continue
                            is_math = bool(re.match(r'^\\\(.*?\\\)$|^\\\[.*?\\\]$|^\$.*?\$', part))
                            if is_math:
                                if part.startswith('\\(') and part.endswith('\\)'):
                                    part = part[2:-2]
                                elif part.startswith('\\[') and part.endswith('\\]'):
                                    part = part[2:-2]
                                elif part.startswith('$') and part.endswith('$'):
                                    part = part[1:-1]
                                processed_line += f"${part}$"
                            else:
                                part = part.replace('\\n', '').replace('\\\\', '')
                                processed_line += f"\\text{{{part}}}"
                        
                        try:
                            text_obj = Tex(processed_line, font_size=font_size, color=subtitle['color'])
                        except Exception as e:
                            print(f"Erro ao renderizar LaTeX: {str(e)}")
                            print(f"Renderizando como texto normal: {line}")
                            text_obj = Text(line, font_size=font_size, color=subtitle['color'])
                    else:
                        line = line.replace('\\n', '').replace('\\\\', '')
                        text_obj = Text(line, font_size=font_size, color=subtitle['color'])
                    
                    scale_factor = font_size / 48.0
                    text_obj.scale(scale_factor * 2)
                    
                    text_obj.align_to([left_margin, current_y, 0], LEFT)
                    print(f"Renderizando linha na posição y={current_y}: {line}")
                    
                    cursor = Circle(radius=0.1, color=WHITE).move_to(text_obj.get_left())
                    cursor.generate_target()
                    cursor.target.move_to(text_obj.get_right())
                    
                    try:
                        animation_time = duration / num_lines
                        if animation_time <= 0:
                            animation_time = 1.0  # Tempo mínimo para evitar erros
                        self.play(
                            AnimationGroup(
                                Write(text_obj, run_time=animation_time),
                                MoveToTarget(cursor, run_time=animation_time)
                            )
                        )
                        self.play(FadeOut(cursor))
                    except Exception as e:
                        print(f"Erro durante a animação: {str(e)}")
                        raise
                    
                    text_objects.append(text_obj)
                    current_y -= line_spacing
                
                y_offset = current_y
                pause_time = max(0, duration - 1)
                self.wait(pause_time)
            
            except Exception as e:
                print(f"Erro ao processar subtitle {subtitle.get('number', 'desconhecido')}: {str(e)}")
                continue
        
        self.wait(2)