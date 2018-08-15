'''
All address used is type str in binary form. E.g. 111011
'''
from abc import ABCMeta, abstractmethod, abstractproperty
import math

class CacheLine:
    def __init__(self, valid=None, tag=None, data=None):
        self._valid = valid
        self._tag = tag
        self._data = data

    def __str__(self):
        len_dash = len(self.tag) + len(str(self.data)) + 11
        dash = '-'*len_dash
        print(dash)
        print('|', int(self.valid), '|', self.tag, '|', self.data, '|')

        return dash


    @property
    def valid(self):
        return self._valid
    @valid.setter
    def valid(self, val):
        self._valid = val

    @property
    def tag(self):
        return self._tag
    @tag.setter
    def tag(self, val):
        self._tag = val

    @property
    def data(self):
        return self._data
    @data.setter
    def data(self, val):
        self._data = val


class Cache(metaclass=ABCMeta):
    def __init__(self, addr_sz, block_sz, num_set):
        self.addr_sz = addr_sz
        self.block_sz = block_sz
        self.num_set = num_set
        self.cache = [None]*num_set

    def parser(self,addr):
        num_offset = int(math.log(self.block_sz,2))
        num_index = int(math.log(self.num_set,2))

        offset = addr[-num_offset:]
        addr = addr[:-num_offset]

        index = addr[-num_index:]
        tag = addr[:-num_index]

        return {'offset': offset, 'index': index, 'tag': tag}

    @abstractmethod
    def display_cache(self):
        pass
    @abstractmethod
    def read_addr(self,addr,data):
        pass
    @abstractmethod
    def write_addr(self,addr,data):
        pass


class directMapped(Cache):
    def read_addr(self, addr, data):
        tokens = self.parser(addr)
        index = int(tokens['index'],2)
        tag = tokens['tag']

        miss = True
        addr_cache_line = CacheLine(True, tag, data)
        if self.cache[index] != None:
            cache_line = self.cache[index]
            if cache_line.valid and cache_line.tag == tag:
                miss = False

        # put data in if miss
        if miss:
            self.cache[index] = addr_cache_line

        print('Reading at addr:', addr, '| miss:', miss)


    def write_addr(self, addr, data):
        read_addr(self, addr, data)

    def display_cache(self):
        for index, line in enumerate(self.cache):
            if line == None:
                self.cache[index] = CacheLine(valid=False, tag='None', data='None')
            print(self.cache[index])


def hex_to_bin(hex):
    '''
    @arg: hex string
    @return: 32 bits
    '''
    base = 16
    decimal = int(hex,base)
    result = bin(decimal)[2:] # [2:] does not include 0xb
    # sign extend the result
    print('result[0]', result[0], result)
    sign = result[0] # most significant bit
    len_to_fill = 32 - len(result)
    sign = sign*len_to_fill
    return sign + result

d = directMapped(32, 4, 16 )
x = 69

with open('test.txt') as f:
    addrs = f.read().split(',')

    for addr in addrs:
        addr = addr.strip()
        addr = addr[2:]
        addr = hex_to_bin(addr)
        d.read_addr(addr, x)

d.display_cache()
