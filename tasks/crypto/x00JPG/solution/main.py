from hashlib import md5
#генерация файла
flag = open("olala.jpg", mode="rb")
result = [md5(bytes([i])).hexdigest() for i in flag.read()]
res = open("result.txt", mode="w+")
for i in result:
    res.write(i)
#решение

dct = dict()
for i in range(256):

    dct[md5(bytes([i])).hexdigest()] = bytes([i])
res = open("result.txt", mode="rb").read().decode()
ans = open("flag.jpg", mode="wb+")
for i in range(0, len(res), 32):
    ans.write(dct[res[i:i + 32]])
