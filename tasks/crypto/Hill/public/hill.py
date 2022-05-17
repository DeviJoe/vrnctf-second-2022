import random
import numpy as np

m = 127
n = 4

mod = np.vectorize(lambda x: x % m)
to_int = np.vectorize(lambda x: round(x))


def generate_matrix():
    a = np.zeros((n, n), dtype=np.int64)
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


if __name__ == '__main__':
    a = generate_matrix()
    secret_text = '********'
    res = encrypt(a, secret_text)
    print(res)
