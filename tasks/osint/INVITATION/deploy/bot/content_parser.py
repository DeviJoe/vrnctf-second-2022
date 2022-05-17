import re

from html.parser import HTMLParser
from io import StringIO
from itertools import combinations_with_replacement
import string


class MLSTripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()


planes_regex = re.compile(r'\b269\b | \b1129\b | \bLM-130\b', flags=re.I | re.X | re.M)

alchemists_regex = re.compile(r'\bagat\b', flags= re.X)

string_regex = re.compile(r'(\s*\b.*\b\s*:\s*\d+\s*.{0,1}\s*\d+\s*.{0,1}\s*(\w\s*\.{0,1}\s*\w|\w)\s*\.{0,1}\s*,\s*\d+\s*.{0,1}\s*\d+\s*.{0,1}\s*(\w\s*\.{0,1}\s*\w|\w)\s*\.{0,1}\s*)', flags= re.I | re.M)
olympus_regex = re.compile(r'(Olympus|Олимп|Olympus\s*Mons)', flags=re.I)
rlyeh_regex = re.compile(r'(Рльех|Р\s*.{1}\s*льех|R\s*.{1}\s*lyeh|Rlyeh)', flags=re.I)
mare_imbrium_regex = re.compile(r'(Mare\s*Imbrium|Море\s*Дождей|Sea\s*of\s*Showers|Sea\s*of\s*Rains)', flags=re.I)
nums_regex = re.compile(r'\d+')

odin_regex = re.compile(r'--\s*(Один|Odin|Óðinn)\s*--\s*(беовульф|Beowulf|Bēowulf)\s*--\s*(Ца́о\s*Ца́о|Цао\s*Цао|曹操|Cáo\s*Cāo|Cao\s*Cao)\s*--\s*(Ахиллес|Ахилл|Achilles|Ἀχιλλεύς)\s*--', flags=re.I)

match_list = [
        (olympus_regex, [[(18, 9, 19, 9)], re.compile("(с.*ш|N)", flags=re.I), [(225, 42, 226, 42)], re.compile("(в.*д|E)", flags=re.I)]),
        (rlyeh_regex, [[(47, 9), (49, 51)], re.compile("(ю.*ш|S)", flags=re.I), [(126, 43), (128, 34)], re.compile("(з.*д|W)", flags=re.I)]),
        (mare_imbrium_regex, [[(22, 0, 43, 0)], re.compile("(c.*ш|N)", flags=re.I), [(5, 0, 26, 0)], re.compile("(з.*д|W)", flags=re.I)])
    ]


def strip_html(input: str):
    stripper = MLSTripper()
    stripper.feed(input)
    return stripper.get_data()


# three words, doesn't matter
def match_planes_task(input: str):
    input = strip_html(input)
    found = planes_regex.findall(input.upper())
    return len(set(found)) == 3


# flag only match
def match_alchemists(input: str):
    input = strip_html(input)
    found = alchemists_regex.findall(input[:1024])
    return len(set(found)) == 1


# --Name: ##°##' с.ш, ##°##' з.д--
def match_cthulhu(input: str):
    input = strip_html(input)

    current_match_idx = 0

    def match_point(actual_point, points_list, required_pos = -1):
        ret = False

        def check_point_pair(point):
            if len(point) == 2:
              return actual_point == point
            elif len(point) == 4:
               curr_point = actual_point[0] << 16 | actual_point[1]
               left_border = point[0] << 16 | point[1]
               right_border = point[2] << 16 | point[3]

               return left_border <= curr_point <= right_border

        if abs(actual_point[0]) > 65535 or abs(actual_point[1]) > 65535:
            return False

        if required_pos >= 0:
            return check_point_pair(points_list[required_pos]), required_pos

        for idx, point_range in enumerate(points_list):
            if check_point_pair(point_range):
               ret = True
               break

        return ret, idx

    duplicated = False

    for res in filter(None, re.split("--", input)):
        for match in string_regex.finditer(res):
            if match_list[current_match_idx][0].search(match.string[match.start(): match.end()]):
                nums = nums_regex.findall(match.string[match.start(): match.end()])

                if duplicated:
                    break

                duplicated = True

                if not match_list[current_match_idx][1][1].match(str(match.group(2))) \
                  or not match_list[current_match_idx][1][3].match(str(match.group(3))):
                    continue

                first_matched, first_match_idx = match_point((int(nums[0]), int(nums[1])), match_list[current_match_idx][1][0])

                if not first_matched\
                  or not match_point((int(nums[2]), int(nums[3])), match_list[current_match_idx][1][2], first_match_idx)[0]:
                    continue

                current_match_idx += 1
                duplicated = False

                if current_match_idx == len(match_list):
                  return True

    return False


# --name1--name2--name3--
def match_odin(input: str):
    input = strip_html(input)
    found = odin_regex.search(input)
    return bool(found)


def get_all_filter_methods():
    return [match_cthulhu, match_odin, match_planes_task, match_alchemists]


def test():
    tests = {match_planes_task:
              {"Гайана 269, LM-130;Аrgentina: 1129 1129": True,
                "269": False,
                "LM-130": False,
                "1129": False,
                "AAAAAAA": False,
                "269LM-1301129": False,
                "269 LM-130 1129": True,
                "<div> 269 LM-130 1129 <p>": True,
                "269\n LM-130\n 1129\n": True,
                "269LM-130112": False,
                "lm-130,lM-130,LM-130": False,
                ", ".join(str(i) for i in range(2000)): False},
            match_alchemists:
                  {"agat": True,
                   "AGAT": False,
                   "agata": False,
                   ','.join(''.join(candidate) for candidate in combinations_with_replacement(string.ascii_lowercase, 4)): False
                   },
            match_cthulhu:
                  {
                    """-- Olympus: 18°   43' с.ш, 225°   43' в.д--
                       -- R’lyeh: 49°   51' ю.ш, 128° 34' з.д--
                       -- Море Дождей: 30° 54' N, 23° 30' W--""": True,
                    """-- Olympus: 18°   43' с.ш, 225°   43' в.д-- -- р.льех: 49°   51' ю.ш, 128° 34' з.д-- -- Море Дождей: 30° 54' N, 23° 30' W--""": True,
                    """-- Olympus: 18°   43' с.ш, 225°   43' в.д--
                       -- р.льех: 47°   9' ю.ш, 128° 34' з.д--
                       -- Море Дождей: 0° 54' N, 23° 30' W-- awdawdawa
                       -- Море Дождей: 30° 54' N, 23° 30' W--""": False, # dup check
                    """-- Olympus: 18°   43' с.ш, 225°   43' в.д--
                       -- р.льех: 47°   9' ю.ш, 128° 34' з.д--
                       -- Море Дождей: 30° 54' N, 23° 30' W--""": False, # R'lyeh check
                    """-- Olympus: 18°43' с.ш, 225°43' з.д--
                       -- рwdawaльех: 47°   9' ю.ш, 128° 34' з.д--
                       -- Море Дождей: 30° 54' N, 23° 30' W--""": False, # Olympus invalid longitude
                    """-- Olym: 18°   43' с.ш, 225°   43' в.д-
                       -- Olympus: 18°   43' с.ш, 225°   43' в.д--
                       -- р.льех: 49°   51' ю.ш, 128° 34' з.д--
                       -- Море Дождей: 30° 54' N, 23° 30' W--""": True,
                    """-- Olym: 18°   43' с.ш, 225°   43' в.д-
                       -- Olympus: 18°   43' с.ш, 225°   43' в.д--
                       -- р.льех: 49°   51' ю.ш, 128° 34' з.д--
                       -- Море Дождей: 30° 54' N, 26° 01' W--""": False,
                    """-- Olym: 18°   43' с.ш, 225°   43' в.д-
                       -- Olympus: 18°   43' с.ш, 225°   43' в.д--
                       -- р.льех: 49°   51' ю.ш, 128° 34' з.д--
                       -- Море Дождей: 30° 54' N, 26° 01' W--""": False,
                  },
            match_odin:
                  {
                    "--Один--Беовульф--Цао Цао--Ахиллес--": True,
                    "--ОдиН--Беовульф--Цао Цао--Ахиллес--": True,
                    "--ОдиН--Беовульф--": False,
                    "--ОдиН--Беовульф--曹操--Ахиллес--": True
                  }}

    for method, test_list in tests.items():
        for test_string, expected_result in test_list.items():
            if method(test_string) != expected_result:
                print(f"Test {test_string} returned {not expected_result}")

    # print(match_cthulhu("""-- Olympus: 18°   43' с.ш, 225°   43' в.д-- -- р.льех: 49°   51' ю.ш, 128° 34' з.д-- -- Море Дождей: 30° 54' N, 23° 30' W--"""))
