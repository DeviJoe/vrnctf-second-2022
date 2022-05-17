import os.path
import bitarray


# Класс создан для хранения предыдущего блока и ксора переданного с предудущим для последующего сохранения
class CBCEncrypter:

    def __init__(self, init_key: bitarray.bitarray) -> None:
        super().__init__()
        # Ключ инициализации
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


class CBCDecrypter:

    def __init__(self, init_key: bitarray.bitarray) -> None:
        super().__init__()
        # Ключ инициализации
        self.key = init_key
        self.prev_block: bitarray.bitarray = None
        self.lazy_block = None

    def save_lazy_block(self, block):
        self.lazy_block = block

    def xor_block(self, block: bitarray.bitarray):
        if self.prev_block is None:
            self.prev_block = self.lazy_block
            return block ^ self.key
        else:
            res = block ^ self.prev_block
            self.prev_block = self.lazy_block
            return res


def read_file_to_bit_arr(filename: str) -> bitarray:
    """
    Считывание файла в битовый массив
    :param filename: имя файла
    :return: битовый массив текста с файла
    """
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
    """
    Считывание ключа из файла. Ожидается, что ключ 64 битный (8 байт)
    :param filename: имя файла
    :return: битовый массив ключа
    """
    filesize = os.path.getsize(filename)
    with open(filename, 'rb') as f:
        bit_arr = bitarray.bitarray(1)
        bit_arr.fromfile(f, filesize)
    return bit_arr[1:]


def ror(value: bitarray, shift: int) -> bitarray:
    """
    Циклический битовый сдвиг вправо
    :param value: битовый массив
    :param shift: значение сдвига
    :return: измененный битовый массив
    """
    shift = shift % len(value)
    right = value[:shift]
    left = value[:-shift]
    return right + left
    pass


def rol(value: bitarray, shift: int) -> bitarray:
    """
    Циклический битовый сдвиг влево
    :param value: битовый массив
    :param shift: значение сдвига
    :return: измененный битовый массив
    """
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
    """
    Функция шифрования сообщиения
    :param minimum_bits_block: размер минимального блока для шифрования (кратно 8)
    :param block_size: размер блока для шифрования (кратно minimum_bytes_block)
    :param msg: сообщение для шифровки
    :param init_key: стартовый ключ для шифования
    :param round_cols: количество раундов шифрования
    :return: зашифрованное сообщение
    """

    # Добивка последнего блока до 64 битов
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

            # Реализация CBC
            block = cbc.xor_block(block)

            # Блок, разбитый на 4 подблока
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


def decrypt(crypto_msg, init_key, iv, round_cols=1, block_size=64, minimum_bits_block=16, clear_output=True):
    """

    :param crypto_msg: зашифрованное сообщение
    :param init_key: начальный ключ инициализации
    :param round_cols: количество раундов
    :param block_size: размер блока для шифрования (кратен minimum_bits_block)
    :param minimum_bits_block: минимальный блок кодирования (кратен 8)
    :param clear_output: очищает вывод от NULL байтов (есть возможность выключить, если сообщение их намеренно содежит)
    :return:
    """
    if minimum_bits_block % 8 != 0 or block_size % minimum_bits_block != 0:
        raise Exception("Неверные размеры блоков для шифрования!!!")

    tail_cell_size = len(crypto_msg) % block_size
    if tail_cell_size != 0:
        crypto_msg += '0' * (block_size - tail_cell_size)

    block_col = len(crypto_msg) // block_size
    decrypt_msg = bitarray.bitarray(0)
    key_vec = gen_key_vector(init_key, round_cols)
    cbc = CBCDecrypter(iv)

    for round_num in range(round_cols):
        for block_num in range(block_col):
            start = block_num * block_size
            end = block_num * block_size + block_size

            block = crypto_msg[start:end]
            cbc.save_lazy_block(block)
            # Блок, разбитый на 4 подблока
            blocks = [block[i * minimum_bits_block: i * minimum_bits_block + minimum_bits_block] for i in range(4)]

            res_block = [None for i in range(4)]

            res_block[0] = blocks[3]
            res_block[1] = blocks[0]
            res_block[2] = blocks[1] ^ blocks[3]
            res_block[3] = (blocks[2] ^ blocks[1]) ^ (key_vec[round_num] ^ blocks[0])

            res = bitarray.bitarray(0)
            for r in res_block:
                res += r

            res = cbc.xor_block(res)

            decrypt_msg += res
        crypto_msg = decrypt_msg
        decrypt_msg = bitarray.bitarray(0)

    decrypt_msg = [crypto_msg[i * 8: i * 8 + 8] for i in range(len(crypto_msg) // 8)]
    NULL = bitarray.bitarray('0' * 8)
    while bitarray.bitarray(NULL) in decrypt_msg:
        decrypt_msg.remove(NULL)

    crypto_msg = bitarray.bitarray(0)
    for partition in decrypt_msg:
        crypto_msg += partition
    return crypto_msg
    pass


def get_iv(data: str):
    iv = bitarray.bitarray(1)
    iv.frombytes(data.encode())
    return iv[1:]


if __name__ == '__main__':
    f = open('iv.txt')
    iv_v = f.readline()
    iv_data = get_iv(iv_v)
    key = read_key('./key.txt')

    crypto = read_file_to_bit_arr('./flag.bin')
    new_text = decrypt(crypto, key, iv_data)
    print("Шифротекст: ", new_text)
    write_bit_arr_to_file(new_text, 'decrypt_message.txt')

    pass
