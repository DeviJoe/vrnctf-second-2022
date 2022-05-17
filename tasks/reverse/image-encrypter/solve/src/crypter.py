import sys
import datetime
import base64
from random import random, seed, shuffle


def write_file(filename, data):
    with open(filename, 'wb') as f:
        f.write(data)
    pass


def load_img(img_path):
    with open(img_path, 'rb') as input_file:
        data = input_file.read()
        return data
        pass
    pass


def load_key(key_path):
    with open(key_path, 'r') as input_file:
        data = input_file.read()
        return data
        pass
    pass


# побить флаг на секции по 32 бийта, собрать секции в массив,
# переставить секции местами по псевдослучайному рандому,
# который в качестве сида принимает время запуска
# поксорить каждый символ с ключом
def encrypt(img, key_str):
    seed_str = str(datetime.datetime.utcnow())
    print(seed_str)
    seed(seed_str, version=2)
    data = []

    a = len(img) / len(key_str)
    for i in range(0, int(len(img) / len(key_str)) + 1):
        part = img[i * len(key_str):(i + 1) * len(key_str)]
        data.append(part)

    shuffle(data)

    res_buf = []
    for elem in data:
        code = [0] * len(key)
        for i, byte in enumerate(elem):
            ch = ord(key_str[i])
            p = byte ^ ch
            code[i] = p
        res_buf.append(bytes(code))

    res = b''
    for part in res_buf:
        res += part

    for i in range(10):
        res = base64.b64encode(res)

    return res
    pass


if __name__ == '__main__':
    if len(sys.argv) != 4:
        exit(-1)
    img_data = load_img(sys.argv[1])
    key = load_key(sys.argv[2])

    enc_data = encrypt(img_data, key)

    write_file(sys.argv[3], enc_data)
    pass
