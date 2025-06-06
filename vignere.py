from manim import *

class VigenereCipherAnimation(Scene):
    def construct(self):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        char_to_index = {c: i for i, c in enumerate(alphabet)}
        n = len(alphabet)

        plaintext = "ATAQUE"
        key =       "CRYPTO"
        extended_key = (key * ((len(plaintext) // len(key)) + 1))[:len(plaintext)]

        # Círculo menor para não sobrescrever a tela
        border_radius = 2.0
        outer_radius = 2.4
        inner_radius = 1.6

        # Alfabeto em círculo
        border_numbers = VGroup()
        outer_letters = VGroup()
        inner_letters = VGroup()
        for i, char in enumerate(alphabet):
            angle =-1* (i-n//4) * TAU / n
            outer_letters.add(
                Text(char, font_size=22).move_to(
                    outer_radius * np.array([np.cos(angle), np.sin(angle), 0])
                ).rotate(angle - PI / 2)  # Base voltada para o centro
            )
            inner_letters.add(
                Text(char, font_size=22).move_to(
                    inner_radius * np.array([np.cos(angle), np.sin(angle), 0])
                ).rotate(angle - PI / 2)
            )
            border_numbers.add(
                Text(str(i), font_size=22).move_to(
                    border_radius * np.array([np.cos(angle), np.sin(angle), 0])
                ).rotate(angle - PI / 2))

        # Letras separadas do plaintext
        plaintext_letters = VGroup(*[
            Text(c, font_size=28).move_to(UP * 3 + RIGHT * (i - len(plaintext) / 2) * 0.6)
            for i, c in enumerate(plaintext)
        ])

        # Letras da chave e seus índices
        key_labels = VGroup()
        key_values = VGroup()
        for i, char in enumerate(extended_key):
            key_char = Text(char, font_size=24)
            # key_val = Text(str(char_to_index[char]), font_size=20, color=YELLOW)
            key_char.move_to(DOWN * 2.9 + RIGHT * (i - len(plaintext) / 2) * 0.6)
            # key_val.next_to(key_char, DOWN, buff=0.1)
            key_labels.add(key_char)
            # key_values.add(key_val)

        # Espaço para escrever texto cifrado
        cipher_label = Text("Ciphertext: ", font_size=24).to_edge(DOWN)
        cipher_letters = VGroup()

        # Círculos
        outer_circle = Circle(radius=outer_radius, color=WHITE)
        inner_circle = Circle(radius=inner_radius, color=BLUE)
        # border_circle = Circle(radius=border_radius, color=BLUE)

        # Apresentação inicial
        self.play(
            LaggedStartMap(FadeIn, plaintext_letters),
            Create(outer_circle),
            Create(inner_circle),
            # Create(border_circle),
        )
        self.play(LaggedStartMap(FadeIn, outer_letters), LaggedStartMap(FadeIn, inner_letters),LaggedStartMap(FadeIn, border_numbers),)
        self.play(FadeIn(key_labels), FadeIn(key_values), Write(cipher_label))

        # # Passo a passo da cifra
        current_inner_rotation = 0  # Track rotation to avoid cumulative drift
        #
        for i, (p_char, k_char) in enumerate(zip(plaintext, extended_key)):
            shift = char_to_index[k_char]
            p_index = char_to_index[p_char]
            c_index = (p_index + shift) % n
            c_char = alphabet[c_index]
        #
        #     # Destaques
            key_highlight = SurroundingRectangle(key_labels[i], color=YELLOW)
            plaintext_highlight = SurroundingRectangle(plaintext_letters[i], color=GREEN)
            plaintext_highlight_outer = SurroundingRectangle(outer_letters[p_index], color=GREEN)
        #
            outer_highlight = SurroundingRectangle(outer_letters[shift], color=YELLOW, buff=0.1)

        #
            self.play(
                Create(key_highlight),
                Create(outer_highlight),
                run_time=0.3
            )

            # Girar disco interno para alinhar
            rotation = (+shift * TAU / n)-current_inner_rotation
            current_inner_rotation += rotation
            self.play(
                Rotate(inner_letters, angle=rotation, about_point=ORIGIN),
                Rotate(inner_circle, angle=rotation, about_point=ORIGIN),
                run_time=1
            )

            # Highlight da letra plaintext no externo
            self.play(
                Create(plaintext_highlight),
                Create(plaintext_highlight_outer),
                run_time=0.5
            )
            self.wait(1)
            # Highlight da letra cifrada no círculo interno
            inner_highlight = SurroundingRectangle(inner_letters[c_index], color=BLUE, buff=0.1)
            self.play(
                Create(inner_highlight),
                run_time=0.5
            )
            self.wait(1)
            # Escreve letra no texto cifrado
            new_letter = Text(c_char, font_size=28).next_to(cipher_label, RIGHT, buff=0.4)
            if cipher_letters:
                new_letter.next_to(cipher_letters[-1], RIGHT, buff=0.2)
            cipher_letters.add(new_letter)
            self.play(Write(new_letter), run_time=0.4)

            # Limpa destaques
            self.play(
                # FadeOut(key_highlight),
                FadeOut(plaintext_highlight),
                FadeOut(plaintext_highlight_outer),
                FadeOut(outer_highlight),
                FadeOut(inner_highlight),
                run_time=0.3
            )
        #
        self.wait(5)
