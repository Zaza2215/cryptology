class Coding:
    __KEY = 18
    __ALPHABET = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя ,._'

    def __init__(self, text=None, ctext=None):
        self.text = text
        self.ctext = ctext

    def caesar_code_i(self, i: str) -> str:
        return self.__ALPHABET[(self.__ALPHABET.index(i) + self.__KEY) % len(self.__ALPHABET)]

    def caesar_code(self):
        text_code = []
        for i in self.text:
            text_code.append(self.caesar_code_i(i))
        self.ctext = ''.join(text_code)

    def caesar_decode_i(self, i: str) -> str:
        return self.__ALPHABET[(self.__ALPHABET.index(i) - self.__KEY) % len(self.__ALPHABET)]

    def caesar_decode(self):
        text_code = []
        for i in self.ctext:
            text_code.append(self.caesar_decode_i(i))
        self.text = ''.join(text_code)


