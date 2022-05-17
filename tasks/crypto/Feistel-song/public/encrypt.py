import os.path
import bitarray


class CBCEncrypter:

    def __init__(self, init_key: bitarray.bitarray) -> None:
        super().__init__()
        self.key = init_key
        self.prev_block: bitarray.bitarray = None

    def save_block(self, block):
        self.prev_block = block

    def xor_block(self, block: bitarray.bitarray):
        if self.prev_block is None:
            return block ^ self.key
        else:
            res = block ^ self.prev_block
            self.prev_block = block
            return res


def read_file_to_bit_arr(filename: str) -> bitarray:
    filesize = os.path.getsize(filename)
    with open(filename, 'rb') as f:
        bit_arr = bitarray.bitarray(1)
        bit_arr.fromfile(f, filesize)
    return bit_arr[1:]
    pass


def write_bit_arr_to_file(crypto_msg, filename='output.crypto'):
    with open(filename, 'wb') as f:
        f.write(crypto_msg)


def read_key(filename: str) -> bitarray:
    filesize = os.path.getsize(filename)
    with open(filename, 'rb') as f:
        bit_arr = bitarray.bitarray(1)
        bit_arr.fromfile(f, filesize)
    return bit_arr[1:]


def ror(value: bitarray, shift: int) -> bitarray:
    shift = shift % len(value)
    right = value[:shift]
    left = value[:-shift]
    return right + left
    pass


def rol(value: bitarray, shift: int) -> bitarray:
    shift = shift % len(value)
    left = value[:shift]
    right = value[shift:]
    return right + left
    pass


def gen_key_vector(secret_key: bitarray, round_col: int):
    res = []
    for i in range(round_col):
        step1 = rol(secret_key, i * 3)
        step2 = bitarray.bitarray(32)
        pointer = 0
        for i, elem in enumerate(step1):
            if i % 2 == 1:
                step2[pointer] = elem
                pointer += 1
        step3 = step2[16:]
        res.append(step3)
    return res
    pass


def encrypt(msg, init_key, iv, round_cols=1, block_size=64, minimum_bits_block=16):
    if minimum_bits_block % 8 != 0 or block_size % minimum_bits_block != 0:
        raise Exception("Неверные размеры блоков для шифрования!!!")

    tail_cell_size = len(msg) % block_size
    if tail_cell_size != 0:
        msg += '0' * (block_size - tail_cell_size)

    block_col = len(msg) // block_size
    crypto_msg = bitarray.bitarray(0)
    key_vec = gen_key_vector(init_key, round_cols)
    cbc = CBCEncrypter(iv)
    for round_num in range(round_cols):
        for block_num in range(block_col):
            start = block_num * block_size
            end = block_num * block_size + block_size
            block = msg[start:end]

            block = cbc.xor_block(block)

            blocks = [block[i * minimum_bits_block: i * minimum_bits_block + minimum_bits_block] for i in range(4)]
            del block
            res_block = [None for i in range(4)]

            res_block[0] = blocks[1]
            res_block[1] = blocks[2] ^ blocks[0]
            res_block[2] = ((blocks[1] ^ key_vec[round_num]) ^ blocks[3]) ^ (blocks[2] ^ blocks[0])
            res_block[3] = blocks[0]

            res = bitarray.bitarray(0)
            for r in res_block:
                res += r

            cbc.save_block(res)
            crypto_msg += res
        msg = crypto_msg
    return msg


def get_iv(data: str):
    iv = bitarray.bitarray(1)
    iv.frombytes(data.encode())
    return iv[1:]


if __name__ == '__main__':
    text = read_file_to_bit_arr('./input_file.txt')
    f = open('iv.txt')
    iv_v = f.readline()
    iv_data = get_iv(iv_v)

    key = read_key('./key.txt')
    text = encrypt(text, key, iv_data)
    write_bit_arr_to_file(text, 'flag.bin')

    pass