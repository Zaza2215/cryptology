from alphabet import Alphabet
from math import gcd


def is_prime(num: int) -> bool:
    if num % 2 == 0:
        return num == 2
    d = 3
    while d * d <= num and num % d:
        d += 2
    return d * d > num


class Crypto:
    _alp = Alphabet('abcdefghijklmnopqrstuvwxyz1234567890 ,.?_')
    _len_alp = len(_alp)

    def __init__(self, text: str = ''):
        self.text = text

    @staticmethod
    def get_inverse_key(a, m):
        for i in range(1, m):
            if a * i % m == 1:
                return i
        return -1

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if isinstance(value, str) and not set(value) - set(self.alp):
            self._text = value
        else:
            raise ValueError(f'text must be string type and all signs of text must be into alphabet: {self.alp}')

    @property
    def alp(self):
        return self._alp

    @alp.setter
    def alp(self, value: str):

        if not isinstance(value, str):
            raise ValueError(f'Expected a string but received an {type(value)}')
        elif len(set(value)) != len(value):
            raise ValueError('Signs are repeated in alphabet')
        else:
            self._alp = value
            self._len_alp = len(value)


class Caesar(Crypto):
    def __init__(self, text: str, key: int):
        self.key = key
        super().__init__(text)

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        if isinstance(value, int):
            self._key = value
        else:
            raise TypeError('Key must be integer')

    def code_i(self, i: str) -> str:
        return self.alp[(self._alp.index(i) + self.key) % self._len_alp]

    def code(self):
        text_code = []
        for i in self.text:
            text_code.append(self.code_i(i))
        return ''.join(text_code)

    def decode_i(self, i: str) -> str:
        return self.alp[(self._alp.index(i) - self.key) % self._len_alp]

    def decode(self):
        text_code = []
        for i in self.text:
            text_code.append(self.decode_i(i))
        return ''.join(text_code)


class Line(Crypto):
    def __init__(self, text: str, key: int):
        super().__init__(text)
        self.key = key
        self._key_decode = self.key ** (self._len_alp - 2) % self._len_alp

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        if isinstance(value, int) and gcd(value, self._len_alp) == 1:
            self._key = value
        else:
            raise ValueError('Key must be integer and length of alphabet with key must be coprime')

    def code_i(self, i: str) -> str:
        return self.alp[(self.alp.index(i) * self.key) % self._len_alp]

    # PROBLEM: first sign of alphabet doesn't encrypt
    def code(self) -> str:
        text_code = []
        for i in self.text:
            text_code.append(self.code_i(i))
        return ''.join(text_code)

    def decode_i(self, i: str) -> str:
        return self.alp[self.alp.index(i) * self._key_decode % self._len_alp]

    def decode(self) -> str:
        text_code = []
        for i in self.text:
            text_code.append(self.decode_i(i))
        return ''.join(text_code)


class Affine(Crypto):
    def __init__(self, text: str, key_1: int, key_2: int):
        super().__init__(text)
        self.key_1 = key_1
        self.key_2 = key_2

    @property
    def key_1(self):
        return self._key_1

    @key_1.setter
    def key_1(self, value):
        if isinstance(value, int) and gcd(value, len(self.alp)) == 1:
            self._key_1 = value
            self._key_decode = self.__class__.get_inverse_key(self.key_1, len(self.alp))
        else:
            raise ValueError('Key must be integer and length of alphabet with key must be coprime')

    @property
    def key_2(self):
        return self._key_2

    @key_2.setter
    def key_2(self, value):
        if isinstance(value, int):
            self._key_2 = value
        else:
            raise TypeError('Key must be integer')

    def code_i(self, i: str) -> str:
        return self.alp[(self.alp.index(i) * self.key_1 + self.key_2) % self._len_alp]

    def code(self):
        text_code = []
        for i in self.text:
            text_code.append(self.code_i(i))
        return ''.join(text_code)

    def decode_i(self, i: str) -> str:
        index = self._key_decode * (self.alp.index(i) + len(self.alp) - self._key_2) % len(self.alp)
        return self.alp[index]

    def decode(self):
        text_code = []
        for i in self.text:
            text_code.append(self.decode_i(i))
        return ''.join(text_code)
