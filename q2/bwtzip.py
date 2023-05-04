# Student Name: Adam Ye
# Student ID: 31460798

from typing import Dict
import sys
ASCII_RANGE = 90


def c2i(s: str) -> int:
    return ord(s)-37


def bwt_encode(s: str):
    s += '$'

    def cyclic_rotation(s: str, start: int):
        return s[start:] + s[:start]

    n = len(s)
    sa = []
    for i in range(n):
        sa.append(cyclic_rotation(s, i))
    sa.sort()

    res = ""
    for s in sa:
        res += s[-1]

    return res


def runlength_encode(s: str):
    n = len(s)
    res = []
    run = 0
    for i in range(n-1):
        if s[i] == s[i+1]:
            run += 1
        else:
            res.append((s[i], run+1))
            run = 0

    if s[n-1] == s[n-2]:
        res.append((s[n-1], run+1))
    else:
        res.append((s[n-1], 1))
    return res


def num2bin(num: int) -> str:
    res = ''
    while num != 0:
        res += str(num % 2)
        num = num // 2
    return res[::-1]


def bin2num(s: str) -> int:
    mult = 1
    res = 0
    for i in range(len(s)-1, -1, -1):
        if s[i] == '1':  # minimal binary code for lengths always start with 0
            res += mult
        mult *= 2
    return res


def elias_encode(num: int) -> str:
    lengths = [num2bin(num)]
    while True:
        length = num2bin(len(lengths[-1])-1)
        if length != 0 and length != '':
            length = '0' + length[1:]
            lengths.append(length)
        else:
            break
    lengths.reverse()
    return ''.join(lengths)


def create_huffman(s: str) -> Dict[str, str]:
    '''Generates dictionary which maps a char to its Huffman binary string'''
    class BinNode:
        def __init__(self, count, chars):
            self.count = count
            self.chars = chars
            self.left: BinNode = None
            self.right: BinNode = None

        def is_leaf(self) -> bool:
            return not (self.left or self.right)

    def get_binary_paths(root: BinNode) -> str:
        path = {}
        if root.left and not root.left.is_leaf():
            r_paths = get_binary_paths(root.left)
            for key in r_paths.keys():
                r_paths[key] = '0' + r_paths[key]
                path.update(r_paths)
        if root.right and not root.right.is_leaf():
            r_paths = get_binary_paths(root.right)
            for key in r_paths.keys():
                r_paths[key] = '1' + r_paths[key]
                path.update(r_paths)
        if root.left and root.left.is_leaf():
            path[root.left.chars] = '0'
        if root.right and root.right.is_leaf():
            path[root.right.chars] = '1'

        return path

    dict_counts = {}
    for ch in s:
        if ch not in dict_counts:
            dict_counts[ch] = 1
        else:
            dict_counts[ch] = dict_counts[ch] + 1

    nodes = [BinNode(count, ch) for ch, count in dict_counts.items()]
    nodes.sort(key=lambda node: node.count)

    while len(nodes) > 1:
        comb_node = BinNode(nodes[0].count + nodes[1].count, nodes[0].chars + nodes[1].chars)
        comb_node.left = nodes[0]
        comb_node.right = nodes[1]
        nodes[0] = comb_node
        nodes.pop(1)
        nodes.sort(key=lambda node: node.count)

    return get_binary_paths(nodes[0])


class BinaryWriter:
    def __init__(self, f):
        self.buffer = ''
        self.f = f

    def push_bits(self, bits: str):
        self.buffer += bits
        self.__write_buffer_bytes()

    def __write_buffer_bytes(self):
        if len(self.buffer) < 8:
            # not enough bits in buffer to write
            return

        while len(self.buffer) >= 8:
            cur_val = bin2num(self.buffer[:8])
            self.f.write(cur_val.to_bytes(length=1, byteorder='big'))
            self.buffer = self.buffer[8:]

    def flush_buffer(self):
        # pad right with 0s to make the buffer 8 bits, then write to file
        self.buffer = self.buffer + '0' * (8 - len(self.buffer))
        self.__write_buffer_bytes()


def full_enc(s: str):
    filename = 'bwtencoded.bin'
    f = open(filename, 'bw+')
    writer = BinaryWriter(f)

    # header
    bwt = bwt_encode(s)
    huffman_dict = create_huffman(bwt)
    writer.push_bits(elias_encode(len(bwt)))
    writer.push_bits(elias_encode(len(huffman_dict)))

    # header - ASCII to Huffman mapping
    for key, val in huffman_dict.items():
        asciicode = num2bin(ord(key))
        asciicode = '0'*(7-len(asciicode)) + asciicode  # pad left with 0s till it is 7 digits long
        writer.push_bits(asciicode)
        writer.push_bits(elias_encode(len(val)))
        writer.push_bits(val)

    asciicode = []
    ecode = []
    huff = []
    for key, val in huffman_dict.items():
        asciicode.append(num2bin(ord(key)))
        ecode.append(elias_encode(len(val)))
        huff.append(val)

    # body - runlength encoded tuples of BWT string
    runs = runlength_encode(bwt)
    for ch, length in runs:
        writer.push_bits(huffman_dict[ch])
        writer.push_bits(elias_encode(length))
    writer.flush_buffer()
    f.close()


if __name__ == '__main__':
    txt_filename = sys.argv[1]
    f = open(txt_filename, 'r')
    txt = f.readline()
    f.close()
    full_enc(txt)
