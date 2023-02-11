class Crypto:
    __KEY = 18
    __KEY_LINE = 17
    __KEY_LINE_DECODE = None
    __A = 25
    __A_DECODE = None
    __B = 17
    __ALPHABET = 'abcdefghijklmnopqrstuvwxyz1234567890 ,.?_'

    def __init__(self, text=None, ctext=None):
        self.text = text
        self.ctext = ctext

    @staticmethod
    def get_inverse_key(a, m):
        for i in range(1, m):
            if ((a % m) * (i % m)) % m == 1:
                return i
        return -1

    @property
    def alphabet(self):
        return self.__ALPHABET

    def caesar_code_i(self, i: str) -> str:
        return self.alphabet[(self.alphabet.index(i) + self.__KEY) % len(self.alphabet)]

    def caesar_code(self):
        text_code = []
        for i in self.text:
            text_code.append(self.caesar_code_i(i))
        self.ctext = ''.join(text_code)

    def caesar_decode_i(self, i: str) -> str:
        return self.alphabet[(self.alphabet.index(i) - self.__KEY) % len(self.alphabet)]

    def caesar_decode(self):
        text_code = []
        for i in self.ctext:
            text_code.append(self.caesar_decode_i(i))
        self.text = ''.join(text_code)

    def line_code_i(self, i: str) -> str:
        return self.alphabet[(self.alphabet.index(i) * self.__KEY_LINE) % len(self.alphabet)]

    def line_code(self):
        text_code = []
        for i in self.text:
            text_code.append(self.line_code_i(i))
        self.ctext = ''.join(text_code)

    def line_decode_i(self, i: str) -> str:
        return self.__ALPHABET[self.alphabet.index(i) * self.__KEY_LINE_DECODE % len(self.alphabet)]

    def line_decode(self):
        text_code = []
        if not self.__KEY_LINE_DECODE:
            self.__KEY_LINE_DECODE = self.__KEY_LINE ** (len(self.alphabet) - 2) % len(self.alphabet)

        for i in self.ctext:
            text_code.append(self.line_decode_i(i))
        self.text = ''.join(text_code)

    def afin_code_i(self, i: str) -> str:
        return self.alphabet[(self.alphabet.index(i) * self.__A + self.__B) % len(self.alphabet)]

    def afin_code(self):
        text_code = []
        for i in self.text:
            text_code.append(self.afin_code_i(i))
        self.ctext = ''.join(text_code)

    def afin_decode_i(self, i: str) -> str:
        index = self.__A_DECODE * (self.__ALPHABET.index(i) + len(self.__ALPHABET) - self.__B) % len(
            self.__ALPHABET)
        return self.__ALPHABET[index]

    def afin_decode(self):
        text_code = []
        if not self.__A_DECODE:
            self.__A_DECODE = self.__class__.get_inverse_key(self.__A, len(self.__ALPHABET))

        for i in self.ctext:
            text_code.append(self.afin_decode_i(i))
        self.text = ''.join(text_code)
