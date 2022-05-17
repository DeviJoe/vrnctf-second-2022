from string import punctuation, whitespace, digits


class Letter:

    def __init__(self, letter, freq) -> None:
        super().__init__()
        self.letter = letter
        self.freq = float(freq)
        self.percent = float(freq) * 100

    def __repr__(self) -> str:
        return f'{self.letter} - {self.percent}'

    def __str__(self) -> str:
        return f'{self.letter} - {self.freq} - {self.percent}'

    def __eq__(self, o: object) -> bool:
        return o.letter == self.letter and o.freq == self.freq


def read_csv(filename):
    f = open(filename)
    lines = f.readlines()
    s = ''
    lines = list(map(lambda x: x[:-1].split(','), lines))
    for i in range(len(lines)):
        lines[i] = Letter(*lines[i][1:])
    f.close()
    return lines


def read_text(filename):
    f = open(filename)
    text = f.read().replace('\n', '')
    f.close()
    return text


def make_frq_table(text):
    frq_map = {}
    letters_count = 0
    for letter in text:
        letter = letter.lower()
        if letter not in whitespace + punctuation + '–«»' + digits:
            if letter in frq_map.keys():
                frq_map[letter] += 1
            else:
                frq_map[letter] = 1
            letters_count += 1
    result = []
    for letter in frq_map.keys():
        result.append(Letter(letter, frq_map[letter] / letters_count))
    
    result.sort(key=lambda x: x.freq, reverse=True)
    return result


def make_fqr_map(frq_table):
    res = {}
    for elem in frq_table:
        res[elem.letter] = elem
    return res


def make_changes(c, frq_c, frq_ideal):
    c_map = make_fqr_map(frq_c)
    ideal_map = make_fqr_map(frq_ideal)
    res = ''
    for j, letter in enumerate(c):
        if letter.lower() in c_map:
            # Взяли букву
            l = c_map[letter.lower()]
            # В i номер буквы
            i = 0
            for i, e in enumerate(frq_c):
                if e == l:
                    break
            changed_letter = frq_ideal[i]
            res += changed_letter.letter.upper()
        else:
            res += letter
    return res


def save_to_file(text, filename):
    f = open(filename, 'w')
    f.write(text)
    f.close()
    

if __name__ == '__main__':
    freq_table_ideal = read_csv('freq_table.csv')
    cipher = read_text('cipher.txt')
    freq_table_cipher = make_frq_table(cipher)
    plain = make_changes(cipher, freq_table_cipher, freq_table_ideal)
    print(plain)
    save_to_file(plain, 'plaintext.txt')
