from alphabet import Alphabet


class Crypto:
    __KEY = 18
    __KEY_LINE = 17
    __KEY_LINE_DECODE = None
    __A = 25
    __A_DECODE = None
    __B = 17
    __ALPHABET = Alphabet("abcdefghijklmnopqrstuvwxyz1234567890 ,.?_")
    __LEN_ALP = len(__ALPHABET)

    def __init__(self, text=None, ctext=None):
        self.text = text
        self.ctext = ctext
        self.__KEY_LINE_DECODE = (
            self.__KEY_LINE ** (self.__LEN_ALP - 2) % self.__LEN_ALP
        )
        self.__A_DECODE = self.__class__.get_inverse_key(self.__A, len(self.__ALPHABET))

    @staticmethod
    def get_inverse_key(a, m):
        for i in range(1, m):
            if a * i % m == 1:
                return i
        return -1

    @property
    def alphabet(self):
        return self.__ALPHABET

    @alphabet.setter
    def alphabet(self, value: str):
        if not isinstance(value, str):
            raise ValueError(f"Expected a string but received an {type(value)}")
        if len(set(value)) != len(value):
            raise ValueError("Signs are repeated in alphabet")
        else:
            self.__ALPHABET = value
            self.__LEN_ALP = len(value)

    def caesar_code_i(self, i: str) -> str:
        return self.alphabet[(self.alphabet.index(i) + self.__KEY) % self.__LEN_ALP]

    def caesar_code(self):
        text_code = []
        for i in self.text:
            text_code.append(self.caesar_code_i(i))
        self.ctext = "".join(text_code)

    def caesar_decode_i(self, i: str) -> str:
        return self.alphabet[(self.alphabet.index(i) - self.__KEY) % self.__LEN_ALP]

    def caesar_decode(self):
        text_code = []
        for i in self.ctext:
            text_code.append(self.caesar_decode_i(i))
        self.text = "".join(text_code)

    def line_code_i(self, i: str) -> str:
        return self.alphabet[
            (self.alphabet.index(i) * self.__KEY_LINE) % self.__LEN_ALP
        ]

    # PROBLEM: first sign of alphabet doesn't encrypt
    def line_code(self):
        text_code = []
        for i in self.text:
            text_code.append(self.line_code_i(i))
        self.ctext = "".join(text_code)

    def line_decode_i(self, i: str) -> str:
        return self.__ALPHABET[
            self.alphabet.index(i) * self.__KEY_LINE_DECODE % self.__LEN_ALP
        ]

    def line_decode(self):
        text_code = []
        for i in self.ctext:
            text_code.append(self.line_decode_i(i))
        self.text = "".join(text_code)

    def affine_code_i(self, i: str) -> str:
        return self.alphabet[
            (self.alphabet.index(i) * self.__A + self.__B) % self.__LEN_ALP
        ]

    def affine_code(self):
        text_code = []
        for i in self.text:
            text_code.append(self.affine_code_i(i))
        self.ctext = "".join(text_code)

    def affine_decode_i(self, i: str) -> str:
        index = (
            self.__A_DECODE
            * (self.__ALPHABET.index(i) + len(self.__ALPHABET) - self.__B)
            % len(self.__ALPHABET)
        )
        return self.__ALPHABET[index]

    def affine_decode(self):
        text_code = []
        for i in self.ctext:
            text_code.append(self.affine_decode_i(i))
        self.text = "".join(text_code)
