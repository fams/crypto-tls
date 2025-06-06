from manim import *
from numpy import array

    class SSSVisualization(Scene):
    def construct(self):
        # Título
        title = Text("Shamir's Secret Sharing", font_size=48).to_edge(UP)
        self.play(Write(title))

        # Eixos para representar o polinômio
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 2200, 500],
            x_length=6,
            y_length=4,
            axis_config={"include_numbers": True}
        ).shift(DOWN * 0.5)
        labels = axes.get_axis_labels(x_label="x", y_label="f(x)")
        self.play(Create(axes), Write(labels))

        # Polinômio usado (f(x) = 123 + 587x + 911x^2)
        poly_eq = MathTex("f(x) = 123 + 587x + 911x^2\\ \text{mod}\ 2087").scale(0.8).next_to(axes, UP)
        self.play(Write(poly_eq))

        # Shares: (1, 1621), (2, 767), (3, 1735), (4, 351), (5, 789)
        coords = [(1, 1621), (2, 767), (3, 1735), (4, 351), (5, 789)]
        points = [
            Dot(axes.coords_to_point(x, y), color=BLUE) for x, y in coords
        ]
        labels = [
            Text(f"P{x} = ({x}, {y})", font_size=24).next_to(p, DOWN) for (x, y), p in zip(coords, points)
        ]

        for point, label in zip(points, labels):
            self.play(FadeIn(point), Write(label))
            self.wait(0.3)

        # Selecionar 3 pontos para reconstrução
        selected = [0, 1, 2]  # indices of points
        highlight_circles = [
            Circle(radius=0.2, color=YELLOW).move_to(points[i].get_center()) for i in selected
        ]
        self.play(*[Create(c) for c in highlight_circles])

        # Criar interpolação visual usando os 3 pontos (sem usar mod 2087)
        # Usamos os pontos (1, 1621), (2, 767), (3, 1735)
        interp_points = [(1, 1621), (2, 767), (3, 1735)]

        def lagrange_poly(x):
            x_vals = [pt[0] for pt in interp_points]
            y_vals = [pt[1] for pt in interp_points]
            total = 0
            for i in range(len(x_vals)):
                xi, yi = x_vals[i], y_vals[i]
                li = 1
                for j in range(len(x_vals)):
                    if i != j:
                        xj = x_vals[j]
                        li *= (x - xj) / (xi - xj)
                total += yi * li
            return total

        poly_graph = axes.plot(lagrange_poly, x_range=[0.8, 3.2], color=RED)
        self.play(Create(poly_graph))

        # Mostrar que a reconstrução de f(0) = segredo = 123
        f0_result = MathTex("f(0) = 123").scale(1.2).to_edge(DOWN)
        self.wait(1)
        self.play(Write(f0_result))
        self.wait(2)

        # Final
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        final_text = Text("O segredo foi recuperado!", font_size=36, color=GREEN)
        self.play(Write(final_text))
        self.wait(2)
