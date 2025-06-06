from manim import *



class MerkleDamgardConstruction(Scene):
    def construct(self):
        # Mensagem original em blocos
        blocks = ["M₁", "M₂", "M₃"]
        block_objs = [Square(side_length=1).set_fill(BLUE, 0.5).set_stroke(BLUE_E).shift(2*i*RIGHT) for i in range(len(blocks))]
        block_labels = [Text(b, font_size=24).move_to(block_objs[i]) for i, b in enumerate(blocks)]

        self.play(*[FadeIn(b) for b in block_objs + block_labels])
        self.wait(0.5)

        # Inicialização do hash
        h_prev = Rectangle(width=1.5, height=1).set_fill(GRAY, 0.3)
        h_prev_label = Text("IV", font_size=24).move_to(h_prev)
        h_prev_group = VGroup(h_prev, h_prev_label).shift(UP * 2)

        self.play(FadeIn(h_prev_group))
        self.wait(0.5)

        # Função de compressão + setas
        states = []
        for i in range(len(blocks)):
            f = Polygon([-0.75,0,0], [0,0.75,0], [0.75,0,0], [0,-0.75,0], color=YELLOW).scale(0.8)
            f_label = Text("f", font_size=24).move_to(f)
            f_group = VGroup(f, f_label).move_to(2*i*RIGHT)

            h_current = Rectangle(width=1.5, height=1).set_fill(GRAY, 0.3).next_to(f_group, DOWN, buff=0.8)
            h_label = Text(f"H{i+1}", font_size=24).move_to(h_current)

            # Arrows
            arrow1 = Arrow(h_prev_group.get_bottom(), f_group.get_top(), buff=0.1)
            arrow2 = Arrow(block_objs[i].get_top(), f_group.get_left(), buff=0.1)
            arrow3 = Arrow(f_group.get_bottom(), h_current.get_top(), buff=0.1)

            self.play(
                FadeIn(f_group),
                GrowArrow(arrow1),
                GrowArrow(arrow2),
                GrowArrow(arrow3),
                FadeIn(h_current),
                FadeIn(h_label)
            )
            self.wait(0.5)

            h_prev_group = VGroup(h_current, h_label)
            states.append(h_prev_group)

        # Resultado final
        digest_box = Rectangle(width=2, height=1).set_fill(GREEN, 0.4).next_to(h_prev_group, DOWN, buff=1)
        digest_label = Text("Digest", font_size=28).move_to(digest_box)

        self.play(
            GrowArrow(Arrow(h_prev_group.get_bottom(), digest_box.get_top(), buff=0.1)),
            FadeIn(digest_box),
            FadeIn(digest_label)
        )
        self.wait(1)

        # Mostrar ataque: extender M₃ com M₄ e continuar de H₃
        extension = Square(side_length=1).set_fill("#FF8C00", 0.5).set_stroke("#FF8C00").next_to(block_objs[-1], RIGHT, buff=1)
        extension_label = Text("M₄", font_size=24).move_to(extension)

        f_attack = Polygon([-0.75,0,0], [0,0.75,0], [0.75,0,0], [0,-0.75,0], color=RED).scale(0.8)
        f_attack_label = Text("f", font_size=24).move_to(f_attack)
        f_attack_group = VGroup(f_attack, f_attack_label).next_to(extension, DOWN, buff=0.8)

        h_attack = Rectangle(width=1.5, height=1).set_fill(RED, 0.4).next_to(f_attack_group, DOWN, buff=0.8)
        h_attack_label = Text("H₄", font_size=24).move_to(h_attack)

        self.play(
            FadeIn(extension),
            FadeIn(extension_label),
            FadeIn(f_attack_group),
            GrowArrow(Arrow(h_prev_group.get_bottom(), f_attack_group.get_top(), buff=0.1)),
            GrowArrow(Arrow(extension.get_top(), f_attack_group.get_left(), buff=0.1)),
            FadeIn(h_attack),
            FadeIn(h_attack_label)
        )
        self.wait(2)

        explanation = Text("Atacante continua a computação a partir de H₃", font_size=24).next_to(h_attack, DOWN)
        self.play(Write(explanation))
        self.wait(3)
