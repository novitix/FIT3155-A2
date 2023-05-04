# Student Name: Adam Ye
# Student ID: 31460798

ASCII_RANGE = 90


def c2i(s: str) -> int:
    return ord(s)-37


def bwt_decode(l: str):
    n = len(l)
    f = ''.join(sorted(l))
    rank = [None]*ASCII_RANGE
    nOcc = [[0 for _ in range(n)] for _ in range(ASCII_RANGE)]

    # compute rank
    for i in range(n):
        if rank[c2i(f[i])] == None:
            rank[c2i(f[i])] = i

    # compute num occurences in s[0,i)
    for i in range(n-1):
        for ch_i in range(ASCII_RANGE):
            nOcc[ch_i][i+1] = nOcc[ch_i][i]
        nOcc[c2i(l[i])][i+1] += 1

    res = ''
    pos = rank[c2i('$')]
    for _ in range(n):
        res += f[pos]
        pos = rank[c2i(l[pos])] + nOcc[c2i(l[pos])][pos]
    res = res[::-1]     # recovered in reverse as insertions are O(n) time
    return res[:-1]     # remove $


def runlength_decode(tuples):
    s = ''
    for ch, count in tuples:
        s += ch*count

    return s


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
        if s[i] == '1' or i == 0:  # minimal binary code for lengths always start with 0
            res += mult
        mult *= 2
    return res


def elias_decode(s: str) -> (int, int):
    next_comp = None
    pos = 0
    read_len = 1
    while s[pos] == '0':
        next_comp = s[pos:pos+read_len]
        pos += read_len
        read_len = bin2num(next_comp) + 1

    value = bin2num(s[pos:pos+read_len])
    return (value, pos+read_len)


def full_dec(s: str) -> str:
    pos = 0
    bwt_length, pos = elias_decode(s[pos:])
    unique_chs, read_len = elias_decode(s[pos:])
    pos += read_len
    huffman_dict = {}
    for _ in range(unique_chs):
        ch = chr(bin2num(s[pos:pos+7].lstrip('0')))
        pos += 7
        huffman_bin_len, read_len = elias_decode(s[pos:])
        pos += read_len
        huffman_bin = s[pos:pos+huffman_bin_len]
        pos += huffman_bin_len
        huffman_dict[huffman_bin] = ch

    res = ''
    while len(res) < bwt_length:
        read_len = 0
        while s[pos:pos+read_len] not in huffman_dict:
            read_len += 1
        ch = huffman_dict[s[pos:pos+read_len]]
        pos += read_len
        run, read_len = elias_decode(s[pos:])
        pos += read_len
        res += ch * run
    res = bwt_decode(res)
    return res


if __name__ == '__main__':
    filename = 'bwtencoded.bin'
    bitstring = ''
    with open(filename, 'rb') as file:
        while True:
            bytes = file.read(1)

            if not bytes:
                break

            cur_int = int.from_bytes(bytes, byteorder='big')
            cur_bitstring = num2bin(cur_int)
            bitstring += '0'*(8-len(cur_bitstring)) + cur_bitstring
    decoded_str = full_dec(bitstring)

    with open('recovered.txt', 'w') as f:
        f.write(decoded_str)
