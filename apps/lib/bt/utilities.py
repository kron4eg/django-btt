from decimal import Decimal
from string import digits
from itertools import takewhile 

class Iterator:
    
    def __init__(self, seq):
        self.seq = seq
        self.index = -1
        
    def __iter__(self):
        return self
    
    def _next(self):
        try:
            return self.seq[self.index + 1]
        except IndexError:
            raise StopIteration
        
    def _previous(self):
        if self.index >= 0:
            return self.seq[self.index]
        else:
            raise StopIteration
        
    def next(self):
        item = self._next()
        self.index += 1
        return item
    
    def previous(self):
        item = self._previous()
        self.index -= 1
        return item
    
    def shift(self, pos=1):
        self.index += pos
        
class SizeConverter:

    postfix = 'bytes'
    postfixes = (
        ('b', ''),
        ('k', 'kilo'),
        ('m', 'mega'),
        ('g', 'giga'),
        ('t', 'tera'),
        ('p', 'peta'),
        ('e', 'exa'),
        ('z', 'zetta'),
        ('y', 'yotta')
    )

    @staticmethod
    def _extract_number(string):
        try:
            num, pfx = string.split()
        except ValueError:
            num = ''.join(x for x in takewhile(lambda x: x in digits or x == '.', string))
            pfx = string.lstrip(num)

        return float(num) if '.' in num else int(num), pfx

    @classmethod
    def _extract_power(cls, bytes):
        if not bytes:
            return (0,) + cls.postfixes[0]

        for pwr, (pfx, pfxv) in enumerate(cls.postfixes):
            result = bytes / float(1024 ** pwr)
            if result and result < 1024:
                break

        return result, pfx, pfxv

    @classmethod
    def to_human(cls, bytes, capitalize=True, verbose=True, split=False, round_to=2):
        result, pfx, pfxv = cls._extract_power(bytes)

        result = Decimal(str(result)).quantize(Decimal('.' + '0' * round_to))
        result = str(result)

        if verbose:
            pfx = pfxv
            cpfx = cls.postfix
        else:
            cpfx = '' if pfx == 'b' else cls.postfix[0]

        if capitalize:
            pfx = pfx.capitalize()
            cpfx = cpfx.capitalize()

        return (result, pfx, cpfx) if split else ' '.join((result, pfx + cpfx))

    @classmethod
    def to_bytes(cls, string):
        num, pfx = cls._extract_number(str(string))

        if not pfx:
            pfx = 'b'

        for pwr, (pfx_, pfxv) in enumerate(cls.postfixes):
            if pfx.lower().startswith(pfx_):
                break

        return int(num * 1024 ** pwr)