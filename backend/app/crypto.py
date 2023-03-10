import sys

from collections import UserString
from math import gcd


def is_prime(num: int) -> bool:
    if num % 2 == 0:
        return num == 2
    d = 3
    while d * d <= num and num % d:
        d += 2
    return d * d > num


class Crypto:
    class Alphabet(UserString):
        def __init__(self, seq: object, flag: str = None):
            """Flag 'a' using in affine cipher.

            :param seq:
            :param flag:
            """
            super().__init__(seq)
            self.flag = flag

        def __getitem__(self, key: int | slice) -> str:
            """
            self.flag = 'a' do not support slice
            :param key:
            :return:
            """
            if self.flag is None or isinstance(key, slice):
                return str(super().__getitem__(key))
            elif self.flag == "l":
                if 0 <= key <= len(self.data):
                    key -= 1
                return str(super().__getitem__(key))

        def index(self, sub, start=0, end=sys.maxsize):
            result = super().index(sub, start, end)
            if self.flag is None:
                return result
            elif self.flag == "l":
                if result == len(self):
                    return 0
                else:
                    return result + 1

    _alp = Alphabet(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 ,.?_"
    )
    _len_alp = len(_alp)

    def __init__(self, text: str = ""):
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
            raise ValueError(
                f"text must be string type and all signs of text must be into alphabet: {self.alp}"
            )

    @property
    def alp(self):
        return self._alp

    @alp.setter
    def alp(self, value: str):
        if not isinstance(value, str):
            raise ValueError(f"Expected a string but received an {type(value)}")
        elif len(set(value)) != len(value):
            raise ValueError("Signs are repeated in alphabet")
        elif set(self.text) - set(value):
            raise ValueError(
                f"All signs of text must be into the new alphabet: {value}\nClear text or set another alphabet"
                f"Necessary characters in the alphabet: {set(self.text) - set(value)}"
            )
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
            raise TypeError("Key must be integer")

    def code_i(self, i: str) -> str:
        return self.alp[(self._alp.index(i) + self.key) % self._len_alp]

    def code(self):
        text_code = []
        for i in self.text:
            text_code.append(self.code_i(i))
        return "".join(text_code)

    def decode_i(self, i: str) -> str:
        return self.alp[(self._alp.index(i) - self.key) % self._len_alp]

    def decode(self):
        text_code = []
        for i in self.text:
            text_code.append(self.decode_i(i))
        return "".join(text_code)


class Line(Crypto):
    _alp = Crypto.Alphabet(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 ,.?_", flag="l"
    )
    _len_alp = len(_alp)

    def __init__(self, text: str, key: int):
        super().__init__(text)
        self._key_decode = None
        self.key = key

    def set_decode_key(self):
        self._key_decode = self.key ** (self._len_alp - 2) % self._len_alp

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        if isinstance(value, int) and gcd(value, self._len_alp) == 1:
            self._key = value
            self.set_decode_key()
        else:
            raise ValueError(
                "Key must be integer and length of alphabet with key must be coprime"
            )

    @property
    def alp(self):
        return self._alp

    @alp.setter
    def alp(self, value: str):
        super(self.__class__, self.__class__).alp.__set__(self, value)
        self.set_decode_key()

    def code_i(self, i: str) -> str:
        return self.alp[(self.alp.index(i) * self.key) % self._len_alp]

    def code(self) -> str:
        text_code = []
        for i in self.text:
            text_code.append(self.code_i(i))
        return "".join(text_code)

    def decode_i(self, i: str) -> str:
        return self.alp[self.alp.index(i) * self._key_decode % self._len_alp]

    def decode(self) -> str:
        text_code = []
        for i in self.text:
            text_code.append(self.decode_i(i))
        return "".join(text_code)


class Affine(Crypto):
    def __init__(self, text: str, key_1: int, key_2: int):
        super().__init__(text)
        self._key_decode = None
        self.key_1 = key_1
        self.key_2 = key_2

    @property
    def key_1(self):
        return self._key_1

    def set_decode_key(self):
        self._key_decode = self.__class__.get_inverse_key(self.key_1, len(self.alp))

    @key_1.setter
    def key_1(self, value):
        if isinstance(value, int) and gcd(value, len(self.alp)) == 1:
            self._key_1 = value
            self.set_decode_key()
        else:
            raise ValueError(
                "Key must be integer and length of alphabet with key must be coprime"
            )

    @property
    def key_2(self):
        return self._key_2

    @key_2.setter
    def key_2(self, value):
        if isinstance(value, int):
            self._key_2 = value
        else:
            raise TypeError("Key must be integer")

    @property
    def alp(self):
        return self._alp

    @alp.setter
    def alp(self, value: str):
        super(self.__class__, self.__class__).alp.__set__(self, value)
        self.set_decode_key()

    def code_i(self, i: str) -> str:
        return self.alp[(self.alp.index(i) * self.key_1 + self.key_2) % self._len_alp]

    def code(self):
        text_code = []
        for i in self.text:
            text_code.append(self.code_i(i))
        return "".join(text_code)

    def decode_i(self, i: str) -> str:
        index = (
            self._key_decode
            * (self.alp.index(i) + len(self.alp) - self._key_2)
            % len(self.alp)
        )
        return self.alp[index]

    def decode(self):
        text_code = []
        for i in self.text:
            text_code.append(self.decode_i(i))
        return "".join(text_code)


__all__ = ["Affine", "Caesar", "Crypto", "Line", "is_prime"]

if __name__ == "__main__":
    pass
