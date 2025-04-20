from manim import Scene, Circle

class TestScene(Scene):
    def construct(self):
        circle = Circle()
        self.add(circle)
        self.wait(1)