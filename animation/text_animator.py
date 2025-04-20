from manim import Scene, Text, Tex, Circle, Write, WHITE, RIGHT, UP, FadeOut, MoveToTarget, AnimationGroup

class TextAnimator(Scene):
    def __init__(self, text, font_size, text_color, timings=None, is_latex=False, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.font_size = font_size
        self.text_color = text_color
        self.timings = timings if timings else []
        self.is_latex = is_latex
        print(f"Usando LaTeX: {self.is_latex}")  # Depuração

    def construct(self):
        # Definir margens fixas
        left_margin = -6.5  # Margem de 0.5 unidades à esquerda (tela vai de x=-7 a x=7)
        right_margin = 5.0  # Margem de 2 unidades à direita
        max_width = right_margin - left_margin  # Largura máxima do texto (11.5 unidades)
        top_margin = 3.6  # Margem de 0.4 unidades no topo (tela vai de y=-4 a y=4)

        if not self.timings:
            # Sem legendas: animação simples com duração fixa
            print("Renderizando texto sem legendas...")
            if self.is_latex:
                try:
                    text_obj = Tex(self.text, font_size=self.font_size, color=self.text_color)
                except Exception as e:
                    print(f"Erro ao renderizar LaTeX (sem legendas): {str(e)}")
                    raise
            else:
                text_obj = Text(self.text, font_size=self.font_size, color=self.text_color)
            # Escala o texto
            scale_factor = self.font_size / 48.0
            text_obj.scale(scale_factor * 2)
            # Limita a largura do texto para respeitar as margens
            text_obj.set_width(min(text_obj.get_width(), max_width))
            # Posiciona o texto no canto superior esquerdo
            text_obj.move_to([left_margin + text_obj.get_width() / 2, top_margin, 0])  # Centro horizontal, y=top_margin
            print(f"Posição do texto: centro={text_obj.get_center()}, topo={text_obj.get_top()}")
            # Sincroniza o cursor com a escrita
            cursor = Circle(radius=0.1, color=WHITE).move_to(text_obj.get_left())
            cursor.generate_target()
            cursor.target.move_to(text_obj.get_right())
            try:
                self.play(
                    AnimationGroup(
                        Write(text_obj, run_time=2),
                        MoveToTarget(cursor, run_time=2)
                    )
                )
                self.play(FadeOut(cursor))
            except Exception as e:
                print(f"Erro durante a animação (sem legendas): {str(e)}")
                raise
            self.wait(1)
        else:
            # Com legendas: acumula frases em linhas diferentes
            y_offset = top_margin  # Começa com 0.4 unidades de margem do topo
            text_objects = []  # Lista para armazenar os objetos de texto
            line_spacing = 1.0  # Espaçamento fixo entre linhas
            for idx, (start_time, end_time, subtitle_text) in enumerate(self.timings):
                print(f"Processando legenda {idx + 1}: {subtitle_text}")
                duration = end_time - start_time
                # Verifica se o texto atingiu a parte inferior (y < -3)
                if y_offset < -3:
                    # Move todos os textos existentes para cima
                    for text_obj in text_objects:
                        text_obj.generate_target()
                        text_obj.target.shift(UP * line_spacing)
                    self.play(
                        *[MoveToTarget(text_obj) for text_obj in text_objects],
                        run_time=0.5
                    )
                    y_offset += line_spacing  # Ajusta y_offset para a nova linha
                # Cria o novo texto
                if self.is_latex:
                    print(f"Texto LaTeX a ser renderizado (legenda): {subtitle_text}")
                    try:
                        text_obj = Tex(subtitle_text, font_size=self.font_size, color=self.text_color)
                    except Exception as e:
                        print(f"Erro ao renderizar LaTeX (legenda): {str(e)}")
                        raise
                else:
                    text_obj = Text(subtitle_text, font_size=self.font_size, color=self.text_color)
                # Escala o texto
                scale_factor = self.font_size / 48.0
                text_obj.scale(scale_factor * 2)
                # Limita a largura do texto para respeitar as margens
                text_obj.set_width(min(text_obj.get_width(), max_width))
                # Posiciona o texto no canto superior esquerdo, ajustando y
                text_obj.move_to([left_margin + text_obj.get_width() / 2, y_offset, 0])  # Centro horizontal, y=y_offset
                print(f"Posição do texto (legenda {idx + 1}): centro={text_obj.get_center()}, topo={text_obj.get_top()}")
                # Sincroniza o cursor com a escrita
                cursor = Circle(radius=0.1, color=WHITE).move_to(text_obj.get_left())
                cursor.generate_target()
                cursor.target.move_to(text_obj.get_right())
                try:
                    self.play(
                        AnimationGroup(
                            Write(text_obj, run_time=duration),
                            MoveToTarget(cursor, run_time=duration)
                        )
                    )
                    self.play(FadeOut(cursor))
                except Exception as e:
                    print(f"Erro durante a animação (legenda {idx + 1}): {str(e)}")
                    raise
                self.wait(max(0, duration - 1))
                text_objects.append(text_obj)
                y_offset -= line_spacing  # Desce uma linha com espaçamento fixo
            self.wait(2)