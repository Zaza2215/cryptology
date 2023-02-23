from unittest import TestCase, main
from math import gcd

from backend.app.crypto import Crypto, Caesar, Line, Affine


class CryptoTest(TestCase):
    def test_basic_caesar(self):
        text = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 ,.?_"
        for key in [-999, -5, -1, 0, 1, 5, 999]:
            s = Caesar(text=text, key=key)
            s.text = s.code()
            self.assertEqual(s.decode(), text)

    def test_basic_line(self):
        text = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 ,.?_"
        for key in [-999, -5, -1, 0, 1, 5, 999]:
            if gcd(key, Line._len_alp) == 1:
                s = Line(text=text, key=key)
                s.text = s.code()
                self.assertEqual(s.decode(), text)
            else:
                self.assertRaises(ValueError)

    def test_basic_affine(self):
        text = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 ,.?_"
        for key_1 in [-999, -5, -1, 0, 1, 5, 999]:
            if gcd(key_1, Affine._len_alp) == 1:
                for key_2 in [-999, -5, -1, 0, 1, 5, 999]:
                    s = Affine(text=text, key_1=key_1, key_2=key_2)
                    s.text = s.code()
                    self.assertEqual(s.decode(), text)
            else:
                self.assertRaises(ValueError)

    # key_caesar = 18
    def test_caesar_code_i(self):
        t = Caesar("", 18)
        self.assertEqual(t.code_i("a"), "s")
        self.assertEqual(t.code_i("_"), "r")
        self.assertEqual(t.code_i("e"), "w")
        self.assertEqual(t.code_i("7"), "j")

    def test_caesar_decode_i(self):
        t = Caesar("", 18)
        self.assertEqual(t.decode_i("s"), "a")
        self.assertEqual(t.decode_i("r"), "_")
        self.assertEqual(t.decode_i("w"), "e")
        self.assertEqual(t.decode_i("j"), "7")

    def test_caesar_code(self):
        t = Caesar(text="a_hello?", key=18)
        self.assertEqual(t.code(), "srzwDDGq")

    def test_caesar_decode(self):
        t = Caesar(text="srzwDDGq", key=18)
        self.assertEqual(t.decode(), "a_hello?")

    # key_line = 17
    def test_line_code_i(self):
        t = Line("", 17)
        self.assertEqual(t.code_i("a"), "q")
        self.assertEqual(t.code_i("_"), "_")
        self.assertEqual(t.code_i("e"), "r")
        self.assertEqual(t.code_i("7"), ".")

    def test_line_decode_i(self):
        t = Line("", 17)
        self.assertEqual(t.decode_i("q"), "a")
        self.assertEqual(t.decode_i("_"), "_")
        self.assertEqual(t.decode_i("r"), "e")
        self.assertEqual(t.decode_i("."), "7")

    def test_line_code(self):
        t = Line(text="a_hello?", key=17)
        self.assertEqual(t.code(), "q_brcc2X")

    def test_line_decode(self):
        t = Line(text="q_brcc2X", key=17)
        self.assertEqual(t.decode(), "a_hello?")

    # key_affine_1 = 25
    # key_affine_2 = 17
    def test_affine_code_i(self):
        t = Affine("", key_1=25, key_2=17)
        self.assertEqual(t.code_i("a"), "r")
        self.assertEqual(t.code_i("_"), "8")
        self.assertEqual(t.code_i("e"), "Y")
        self.assertEqual(t.code_i("7"), "9")

    def test_affine_decode_i(self):
        t = Affine("", key_1=25, key_2=17)
        self.assertEqual(t.decode_i("r"), "a")
        self.assertEqual(t.decode_i("8"), "_")
        self.assertEqual(t.decode_i("Y"), "e")
        self.assertEqual(t.decode_i("9"), "7")

    def test_affine_code(self):
        t = Affine(text="a_hello?", key_1=25, key_2=17)
        self.assertEqual(t.code(), "r87YyyGI")

    def test_affine_decode(self):
        t = Affine(text="r87YyyGI", key_1=25, key_2=17)
        self.assertEqual(t.decode(), "a_hello?")

    def test_get_invert_key(self):
        self.assertEqual(Crypto.get_inverse_key(5, 29), 6)
        self.assertEqual(Crypto.get_inverse_key(5, 26), 21)

    def test_alphabet(self):
        t = Crypto()
        t.alp = "abcdefgh"
        self.assertEqual(t.alp, "abcdefgh")

    def test_alphabet_raises(self):
        values = [["a", "b", "c"], ("a", "b", "c"), 123, 32.1, {"a": 1, "b": 2}]
        t = Crypto()
        for value in values:
            with self.assertRaises(ValueError) as ex:
                t.alp = value
                self.assertEqual(
                    f"Expected a string but received an {type(value)}",
                    ex.exception.args[0],
                )
        with self.assertRaises(ValueError) as ex:
            value = "abcdefghh"
            t.alp = value
        self.assertEqual("Signs are repeated in alphabet", ex.exception.args[0])

    def test_alphabet_len(self):
        t = Crypto()
        self.assertEqual(len(t.alp), t._len_alp)
        value = "abcdefgh"
        t.alp = value
        self.assertEqual(len(t.alp), t._len_alp)

    def test_change_alp(self):
        text = "hello_a"
        line_t = Line(text, 10)
        line_t.alp = "abcdefghijklmnopqrstuvwxyz123456 ,.?_"
        line_t.text = line_t.code()
        self.assertEqual(text, line_t.decode())
        affine_t = Affine(text, 10, 4)
        affine_t.alp = "abcdefghijklmnopqrstuvwxyz123456 ,.?_"
        affine_t.text = affine_t.code()
        self.assertEqual(text, affine_t.decode())

    def test_wrong_text_with_new_alphabet(self):
        text = "Hello_a?"
        line_t = Line(text, 15)
        affine_t = Affine(text, 17, 16)
        with self.assertRaises(ValueError) as ex:
            line_t.alp = "abcdefghijklmnopqrstuvwxyz123456 ,.?_"
        with self.assertRaises(ValueError) as ex:
            affine_t.alp = "abcdefghijklmnopqrstuvwxyz123456 ,.?_"

    if __name__ == "__main__":
        main()
