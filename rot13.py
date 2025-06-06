from manim import *

class Rot13WithHighlight(Scene):
    def construct(self):
        alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        n = len(alphabet)

        # Círculos
        outer_radius = 3
        inner_radius = 2.4

        outer_circle = Circle(radius=outer_radius, color=WHITE)
        inner_circle = Circle(radius=inner_radius, color=BLUE)
        self.play(Create(outer_circle), Create(inner_circle))

        outer_letters = []
        inner_letters = []
        angle_map = {}

        for i, letter in enumerate(alphabet):
            angle = 2 * PI * i / n - PI / 2
            outer_pos = outer_circle.point_at_angle(angle)
            inner_pos = inner_circle.point_at_angle(angle)

            outer_txt = Text(letter, font_size=24)
            outer_txt.move_to(outer_pos)
            outer_txt.rotate(angle - PI/2)
            outer_letters.append(outer_txt)

            inner_txt = Text(letter, font_size=24)
            inner_txt.move_to(inner_pos)
            inner_txt.rotate(angle - PI/2)
            inner_letters.append(inner_txt)

            angle_map[letter] = i

        self.play(*[Write(l) for l in outer_letters])
        self.play(*[Write(l) for l in inner_letters])
        self.wait(0.5)

        # Gira o círculo interno 13 posições (180°)
        self.play(Rotate(VGroup(*inner_letters), angle=PI, about_point=ORIGIN), run_time=2)
        self.wait(1)

        # ROT13 map
        rot13_map = {}
        for i, letter in enumerate(alphabet):
            rot13_map[letter] = alphabet[(i + 13) % 26]

        # Palavra a codificar
        palavra = "SEGREDO"
        palavra_rot13 = "".join([rot13_map[c] for c in palavra])

        # Mostrar palavra no centro dos círculos
        original_letters = VGroup(*[
            Text(c, font_size=36) for c in palavra
        ]).arrange(RIGHT, buff=0.25).move_to(ORIGIN)

        self.play(*[Write(l) for l in original_letters])
        self.wait(0.5)

        # Transformar letra por letra com destaque nos discos
        for i, letra in enumerate(palavra):
            idx = angle_map[letra]
            rot_idx = angle_map[rot13_map[letra]]

            # Cópias destacadas (bordas)
            highlight_orig = SurroundingRectangle(outer_letters[idx], color=YELLOW, buff=0.1)
            highlight_rot = SurroundingRectangle(inner_letters[rot_idx], color=GREEN, buff=0.1)

            self.play(Create(highlight_orig), run_time=0.2)
            self.play(Create(highlight_rot), run_time=0.2)

            nova_letra = Text(rot13_map[letra], font_size=36, color=YELLOW)
            nova_letra.move_to(original_letters[i].get_center())

            self.play(Transform(original_letters[i], nova_letra), run_time=0.5)
            self.wait(0.2)

            self.play(FadeOut(highlight_orig), FadeOut(highlight_rot))

        # Mostrar resultado final
        resultado = Text(f"{palavra} → {palavra_rot13}", font_size=36, color=BLUE)
        resultado.next_to(original_letters, DOWN)
        self.play(Write(resultado))
        self.wait(3)
