import random
import numpy as np

m = 127
n = 4

mod = np.vectorize(lambda x: x % m)
to_int = np.vectorize(lambda x: round(x))


def generate_matrix():
    a = np.zeros((n, n), dtype=np.int64)
    seed = 2201061276
    random.seed(seed)
    det = 0
    while det % m == 0:
        for i in range(a.shape[0]):
            for j in range(a.shape[1]):
                a[i, j] = random.randint(0, m - 1)
        det = round(np.linalg.det(a))
    return a


def process_text(st):
    if len(st) % n != 0:
        st += "".join([" "] * (n - len(st) % n))
    text = [ord(ch) for ch in st]
    return np.array(text).T


def encrypt(a, st: str) -> str:
    text = process_text(st)
    encrypted = ""

    for i in range(0, len(text) - n + 1, n):
        batch_encrypted = a.dot(text[i: i + n])
        encrypted_batch = "".join(
            chr(num % m) for num in batch_encrypted
        )
        encrypted += encrypted_batch

    return encrypted


def inv_matr(a):
    det = round(np.linalg.det(a))
    if det < 0:
        det = det % m

    det_inv = None
    for i in range(m):
        if (det * i) % m == 1:
            det_inv = i
            break
    inv_key = (det_inv * det * np.linalg.inv(a))
    inv_a = to_int(mod(inv_key))
    return inv_a


def get_matr(text):
    r = process_text(text)
    matr = []
    for i in range(0, len(r), n):
        matr.append(r[i:i + n])
    matr = matr[:n]
    return np.array(matr)


if __name__ == '__main__':
    sres = '0nOr.>S]r[Lq:Nhl!'  ##"vrnctf{h1ll_gr3at}"
    secret_text = "Kikoriki known in the United States as GoGoRiki or BalloonToons and in Russia as Smeshariki"
    res = '''$[6%dx-CT1@]|:$#bMSB:JrJN2>P9y[bN>mHH:7b1{ogYyFA	61V]5&)Gm1i |\0[bN>'''
    p = get_matr(secret_text)
    c = get_matr(res)
    key = mod(inv_matr(p) @ c).T
    print(encrypt(inv_matr(key), sres))

# полезные ссылки:
# https://habr.com/ru/post/595281/
# https://github.com/TheAlgorithms/Python/blob/master/ciphers/hill_cipher.py