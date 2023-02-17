from unittest import TestCase, main
from math import gcd

from backend.app.crypto import Crypto, Caesar, Line, Affine


class CryptoTest(TestCase):
    def test_basic_caesar(self):
        text = "abcdefghijklmnopqrstuvwxyz1234567890 ,.?_"
        for key in [-999, -5, -1, 0, 1, 5, 999]:
            s = Caesar(text=text, key=key)
            s.text = s.code()
            self.assertEqual(s.decode(), text)

    def test_basic_line(self):
        text = "abcdefghijklmnopqrstuvwxyz1234567890 ,.?_"
        for key in [-999, -5, -1, 0, 1, 5, 999]:
            if gcd(key, Line._len_alp) == 1:
                s = Line(text=text, key=key)
                s.text = s.code()
                self.assertEqual(s.decode(), text)
            else:
                self.assertRaises(ValueError)

    def test_basic_affine(self):
        text = "abcdefghijklmnopqrstuvwxyz1234567890 ,.?_"
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
        self.assertEqual(t.code(), "srzw447q")

    def test_caesar_decode(self):
        t = Caesar(text="srzw447q", key=18)
        self.assertEqual(t.decode(), "a_hello?")

    # key_line = 17
    def test_line_code_i(self):
        t = Line("", 17)
        self.assertEqual(t.code_i("a"), "a")
        self.assertEqual(t.code_i("_"), "y")
        self.assertEqual(t.code_i("e"), "2")
        self.assertEqual(t.code_i("7"), "l")

    def test_line_decode_i(self):
        t = Line("", 17)
        self.assertEqual(t.decode_i("a"), "a")
        self.assertEqual(t.decode_i("y"), "_")
        self.assertEqual(t.decode_i("2"), "e")
        self.assertEqual(t.decode_i("l"), "7")

    def test_line_code(self):
        t = Line(text="a_hello?", key=17)
        self.assertEqual(t.code(), "ay,2xx8h")

    def test_line_decode(self):
        t = Line(text="ay,2xx8h", key=17)
        self.assertEqual(t.decode(), "a_hello?")

    # key_affine_1 = 25
    # key_affine_2 = 17
    def test_affine_code_i(self):
        t = Affine("", key_1=25, key_2=17)
        self.assertEqual(t.code_i("a"), "r")
        self.assertEqual(t.code_i("_"), "8")
        self.assertEqual(t.code_i("e"), "0")
        self.assertEqual(t.code_i("7"), ".")

    def test_affine_decode_i(self):
        t = Affine("", key_1=25, key_2=17)
        self.assertEqual(t.decode_i("r"), "a")
        self.assertEqual(t.decode_i("8"), "_")
        self.assertEqual(t.decode_i("0"), "e")
        self.assertEqual(t.decode_i("."), "7")

    def test_affine_code(self):
        t = Affine(text="a_hello?", key_1=25, key_2=17)
        self.assertEqual(t.code(), "r830ff?i")

    def test_affine_decode(self):
        t = Affine(text="r830ff?i", key_1=25, key_2=17)
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

    if __name__ == "__main__":
        main()
