from manim import Scene, Tex

class LatexRenderer(Scene):
    def __init__(self, latex_text, font_size, text_color):
        super().__init__()
        self.latex_text = latex_text
        self.font_size = font_size
        self.text_color = text_color

    def construct(self):
        tex = Tex(self.latex_text, font_size=self.font_size, color=self.text_color)
        self.play(Write(tex))
        self.wait(1)