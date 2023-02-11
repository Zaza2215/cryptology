from unittest import TestCase, main
from crypto import Crypto


class CryptoTest(TestCase):

    # key_caesar = 18
    def test_caesar_code_i(self):
        t = Crypto()
        self.assertEqual(t.caesar_code_i('a'), 's')
        self.assertEqual(t.caesar_code_i('_'), 'r')
        self.assertEqual(t.caesar_code_i('e'), 'w')
        self.assertEqual(t.caesar_code_i('7'), 'j')

    def test_caesar_decode_i(self):
        t = Crypto()
        self.assertEqual(t.caesar_decode_i('s'), 'a')
        self.assertEqual(t.caesar_decode_i('r'), '_')
        self.assertEqual(t.caesar_decode_i('w'), 'e')
        self.assertEqual(t.caesar_decode_i('j'), '7')

    def test_caesar_code(self):
        t = Crypto(text='a_hello?')
        t.caesar_code()
        self.assertEqual(t.ctext, 'srzw447q')

    def test_caesar_decode(self):
        t = Crypto(ctext='srzw447q')
        t.caesar_decode()
        self.assertEqual(t.text, 'a_hello?')

    # key_line = 17
    def test_line_code_i(self):
        t = Crypto()
        self.assertEqual(t.line_code_i('a'), 'a')
        self.assertEqual(t.line_code_i('_'), 'y')
        self.assertEqual(t.line_code_i('e'), '2')
        self.assertEqual(t.line_code_i('7'), 'l')

    def test_line_decode_i(self):
        t = Crypto()
        self.assertEqual(t.line_decode_i('a'), 'a')
        self.assertEqual(t.line_decode_i('y'), '_')
        self.assertEqual(t.line_decode_i('2'), 'e')
        self.assertEqual(t.line_decode_i('l'), '7')

    def test_line_code(self):
        t = Crypto(text='a_hello?')
        t.line_code()
        self.assertEqual(t.ctext, 'ay,2xx8h')

    def test_line_decode(self):
        t = Crypto(ctext='ay,2xx8h')
        t.line_decode()
        self.assertEqual(t.text, 'a_hello?')

    # key_afin_1 = 25
    # key_afin_2 = 17
    def test_afin_code_i(self):
        t = Crypto()
        self.assertEqual(t.afin_code_i('a'), 'r')
        self.assertEqual(t.afin_code_i('_'), '8')
        self.assertEqual(t.afin_code_i('e'), '0')
        self.assertEqual(t.afin_code_i('7'), '.')

    def test_afin_decode_i(self):
        t = Crypto()
        self.assertEqual(t.afin_decode_i('r'), 'a')
        self.assertEqual(t.afin_decode_i('8'), '_')
        self.assertEqual(t.afin_decode_i('0'), 'e')
        self.assertEqual(t.afin_decode_i('.'), '7')

    def test_afin_code(self):
        t = Crypto(text='a_hello?')
        t.afin_code()
        self.assertEqual(t.ctext, 'r830ff?i')

    def test_afin_decode(self):
        t = Crypto(ctext='r830ff?i')
        t.afin_decode()
        self.assertEqual(t.text, 'a_hello?')

    def test_get_invert_key(self):
        self.assertEqual(Crypto.get_inverse_key(5, 29), 6)
        self.assertEqual(Crypto.get_inverse_key(5, 26), 21)
        self.assertEqual(Crypto.get_inverse_key(5, 26), 21)
        self.assertEqual(Crypto.get_inverse_key(5, 26), 21)

