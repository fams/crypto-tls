from manim import *

class CryptoCommunication(Scene):
    def construct(self):
        alice = Text("Alice", font_size=36).to_edge(LEFT)
        bob = Text("Bob", font_size=36).to_edge(RIGHT)
        self.play(Write(alice), Write(bob))

        plaintext = Text("Olá, Bob!", font_size=32).next_to(alice, RIGHT, buff=1)
        arrow_to_encrypt = Arrow(start=alice.get_right(), end=plaintext.get_left(), buff=0.1)

        self.play(GrowArrow(arrow_to_encrypt), FadeIn(plaintext))
        self.wait(0.5)

        # Criptografando
        ciphertext = Text("🔒 Mensagem", font_size=32, color=BLUE, font="Segoe UI Emoji")
        ciphertext.move_to(plaintext.get_center())
        self.play(Transform(plaintext, ciphertext))
        self.wait(0.5)

        # Enviando a mensagem
        arrow_to_bob = Arrow(start=plaintext.get_right(), end=bob.get_left(), buff=0.2)
        self.play(GrowArrow(arrow_to_bob))
        self.play(plaintext.animate.move_to(bob.get_left() + LEFT * 1.5))
        self.wait(0.5)

        # Descriptografando
        decrypted = Text("🔓 Olá, Bob!", font_size=32, color=GREEN, font="Segoe UI Emoji").move_to(plaintext.get_center())
        self.play(Transform(plaintext, decrypted))
        self.wait(1)

        self.play(FadeOut(plaintext), FadeOut(arrow_to_encrypt), FadeOut(arrow_to_bob))
