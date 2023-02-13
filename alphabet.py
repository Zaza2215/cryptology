import sys
from collections import UserString


class Alphabet(UserString):
    def __init__(self, seq: object, flag: str = None):
        """
        flag 'a' using in affine cipher
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
        elif self.flag == 'a':
            if 0 <= key <= len(self.data):
                key -= 1
            return str(super().__getitem__(key))

    def index(self, sub, start=0, end=sys.maxsize):
        result = super().index(sub, start, end)
        if self.flag is None:
            return result
        elif self.flag == 'a':
            if result == len(self):
                return 0
            else:
                return result + 1
