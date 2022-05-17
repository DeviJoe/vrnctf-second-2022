import os

if __name__ == '__main__':

    # images = []
    # for i in range(1, 16):
    #     filename = 'flag/'
    #     outname = ''
    #     if i // 10 == 0:
    #         filename += '0'
    #         outname += '0'
    #     filename += str(i) + '.png'
    #     outname += str(i)
    # 
    #     os.system('gzip -9 -c ' + filename + ' > out/' + outname)

    # ART! 8 байт, потом количество изображений 8 байт, потом
    res = b''
    f = open('header', 'rb')
    res += f.read()
    for i in range(1, 16):
        outname = 'out/'
        if i // 10 == 0:
            outname += '0'
        outname += str(i)
        f = open(outname, 'rb')
        res += f.read()
    f = open('flag.art', 'wb')
    f.write(res)
    f.close()