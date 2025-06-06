from manim import *

class SPNConfusionDiffusion(Scene):
    def construct(self):
        colors = [RED, GREEN, BLUE, YELLOW]
        xor_result_colors = [PURPLE, TEAL, ORANGE, MAROON]

        # Entrada
        entrada_blocks = VGroup(*[
            Square(side_length=0.8, fill_opacity=0.8, fill_color=colors[i], stroke_color=WHITE)
            for i in range(4)
        ]).arrange(RIGHT, buff=0.3)
        entrada_label = Text("Entrada", font_size=32).next_to(entrada_blocks, UP, buff=0.3)
        entrada_group = VGroup(entrada_label, entrada_blocks).to_edge(UP, buff=0.5)

        # XOR symbols
        xor_symbols = VGroup(*[
            Text("⊕", font_size=32).next_to(entrada_blocks[i], DOWN, buff=0.7)
            for i in range(4)
        ])
        addroundkey_label = Text("Mistura com chave (AddRoundKey)", font_size=28).next_to(xor_symbols, UP, buff=0.2)

        # Chave única com seta
        chave_k = Text("Chave K₀", font_size=24).next_to(xor_symbols, RIGHT, buff=0.6)
        chave_seta = Arrow(start=chave_k.get_left(), end=xor_symbols[3].get_right(), buff=0.1)

        # Resultado do XOR (AddRoundKey)
        xor_output_blocks = VGroup(*[
            Square(side_length=0.8, fill_opacity=0.8, fill_color=xor_result_colors[i], stroke_color=WHITE)
            for i in range(4)
        ]).arrange(RIGHT, buff=0.3).next_to(entrada_blocks, DOWN, buff=1.4)
        xor_output_label = Text("Resultado (⊕)", font_size=28).next_to(xor_output_blocks, UP, buff=0.1)

        # Confusao (S-box)
        confusao_blocks = VGroup(*[
            Square(side_length=0.8, fill_opacity=0.8, fill_color=xor_result_colors[i], stroke_color=WHITE)
            for i in range(4)
        ]).arrange(RIGHT, buff=0.3).next_to(xor_output_blocks, DOWN, buff=0.6)
        confusao_labels = VGroup(*[
            Text(f"S({i})", font_size=24).move_to(confusao_blocks[i])
            for i in range(4)
        ])
        confusao_label = Text("Confusão (S-box)", font_size=32).next_to(confusao_blocks, UP, buff=0.2)

        # MixColumns: cada entrada afeta todas as saídas (linhas cruzadas)
        mixcolumns_blocks = VGroup(*[
            Square(side_length=0.8, fill_opacity=0.8, fill_color=WHITE, stroke_color=WHITE)
            for _ in range(4)
        ]).arrange(RIGHT, buff=0.3).next_to(confusao_blocks, DOWN, buff=1.5)
        mixcolumns_label = Text("Difusão (MixColumns)", font_size=32).next_to(mixcolumns_blocks, UP, buff=0.2)

        all_lines = VGroup()
        for i in range(4):
            for j in range(4):
                line = Line(confusao_blocks[i].get_bottom(), mixcolumns_blocks[j].get_top(), color=colors[i], stroke_opacity=0.5)
                all_lines.add(line)

        # Animação
        self.play(FadeIn(entrada_group))
        self.wait(1)

        self.play(FadeIn(xor_symbols), FadeIn(addroundkey_label), FadeIn(chave_k), FadeIn(chave_seta))
        self.wait(1)

        self.play(TransformFromCopy(entrada_blocks, xor_output_blocks), FadeIn(xor_output_label))
        self.wait(1)

        self.play(TransformFromCopy(xor_output_blocks, confusao_blocks), FadeIn(confusao_labels), Write(confusao_label))
        self.wait(1)

        self.play(FadeIn(mixcolumns_blocks), FadeIn(mixcolumns_label), *[Create(line) for line in all_lines])
        self.wait(2)
