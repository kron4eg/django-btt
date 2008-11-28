from itertools import takewhile, islice
from string import digits
from types import *

from utilities import Iterator

class InvalidDataError(Exception):
    pass

class Decoder:
    
    @staticmethod
    def string(flow):
        length = int(''.join(takewhile(lambda x: x != ':', flow)))
        string = ''.join(islice(flow, length))
        return string
    
    @staticmethod
    def integer(flow):
        flow.shift()    # skipping 'i'
        integer = int(''.join(takewhile(lambda x: x != 'e', flow)))
        return integer
    
    @classmethod
    def list(cls, flow):
        flow.shift()    # skipping 'l'
        list = []
        for x in flow:
            if x == 'e':
                break
            else:
                flow.shift(-1)
            list.append(cls.get_decoder(x)(flow))
        return list
    
    @classmethod
    def dictionary(cls, flow):
        flow.shift()    # skipping 'd'
        dictionary = {}
        for x in flow:
            if x == 'e':
                break
            else:
                flow.shift(-1)
            key = cls.get_decoder(x)(flow)
            value = cls.get_decoder(flow._next())(flow)
            dictionary[key] = value
        return dictionary
        
    @classmethod
    def get_decoder(cls, x):
        if x in digits:
            return cls.string
        elif x == 'i':
            return cls.integer
        elif x == 'l':
            return cls.list
        elif x == 'd':
            return cls.dictionary
        else:
            raise InvalidDataError
    
    @classmethod
    def decode(cls, data):
        return cls.get_decoder(data[0])(Iterator(data))
    
class Encoder:
    
    @staticmethod
    def string(data):
        return '%i:%s' %(len(data), data)
    
    @staticmethod
    def integer(data):
        return 'i%ie' %data
    
    @classmethod
    def list(cls, data):
        return 'l%se' %''.join(cls.encode(x) for x in data)
    
    @classmethod
    def dictionary(cls, data):
        edata = (cls.encode(key) + cls.encode(data[key]) for key in sorted(data.keys()))
        return 'd%se' %''.join(edata)
    
    @classmethod
    def get_encoder(cls, x):
        if x in (StringType, StringTypes):
            return cls.string
        elif x in (IntType, LongType):
            return cls.integer
        elif x in (ListType, TupleType):
            return cls.list
        elif x is DictType:
            return cls.dictionary
        else:
            raise InvalidDataError
    
    @classmethod
    def encode(cls, data):
        return cls.get_encoder(type(data))(data)
    
def decode(data):
    """Decoded bencoded data"""
    try:
        return Decoder.decode(data)
    except:
        raise InvalidDataError
    
def encode(data):
    """Encode data to bencoding"""
    try:
        return Encoder.encode(data)
    except:
        raise InvalidDataError
