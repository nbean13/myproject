from manim import *


class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        square.flip(RIGHT)
        square.rotate(-3 * TAU / 8)
        circle.set_fill(PINK, opacity=0.5)

        self.play(Create(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))


class YoutubeDemo(Scene):
    def construct(self):
        circle = Circle()
        square = Square()

        text = Text("Hello World", font_size=72)
        text.to_edge(UP)

        self.play(
            Write(text, run_time=3)
        )
        self.play(
            Transform(text[0], circle), 
            run_time=5,
            rate_func=smooth,
        )
