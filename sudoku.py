#!/usr/bin/env python3
# coding=utf-8

# TODO: Translate to lingua franca by PEP8 (comments only)
# TODO: продумать превращение содерждимого основного цикла в одну или несколько функций,
#   вызываемых из более фундаментального цикла.
# TODO: Строку нужно будет получать иначе - из файла, командной строки или интерактивно, туда же — проверку ввода.
#   (СТРОГО ЖЕЛАТЕЛЬНО — интерактивно)
# TODO: добавить исключение возможного значения без собственно простановки символа
#   (если ясно, что в некоторых клетках число стоять не может в любом случае)
# TODO: добавить эвристическое ветвление в случае, если обычными тактиками головоломка не решается.
#   При возвращении от эвристики следует учесть, что возможны три варианта:
#   1. головоломка решена (йух-ху, мы выиграли, возвращаться не надо),
#   2. В головоломке появились явные ошиби
#       (не имеет валидных решений, следовательно необходимо исключить изначальный выбор),
#   3. Головоломка не решена, но и не имеет видимых ошибок
#       (следует запомнить расклад и вернуться к изначальной схеме не изменяя её;
#       если ни одно из стартовых допущений не приведёт к решению или ошибкам, то можно будет выбрать одну из этих веток
#       (желательно наиболее заполненную) для повтора ветвления).
#       Следует так же иметь в виду, что головолома может оказаться В ПРИНЦИПЕ нерешаемой,
#       хотя и будет проходить обычные проверки.
import copy  # To combat the main Python's rake!


class Puzzle:
    def __init__(self, x_size, y_size, chars, puzzle_line):
        self.x = x_size
        self.y = y_size
        self.size = x_size * y_size
        self.chars = chars
        # Preparing field: doing array size×size of '0'
        self.field = [['0' for i1 in range(self.size)] for j1 in range(self.size)]
        # Preparing array of possible values: array size×size of sets with all possible chars
        self.possibles = [[set(chars) for i1 in range(self.size)] for j1 in range(self.size)]
        arr = []
        # Basic puzzle check
        for i1 in puzzle_line.split():
            arr.append(i1)
        if len(arr) != self.size:
            exit('Неправильное количество строк! ВЫХОД.' + str(len(self.field)))
        for i1 in range(self.size):
            if len(arr[i1]) != self.size:
                exit('В строке ' + str(i1 + 1) + ' неправильное количество столбцов! ВЫХОД.')
            for j1 in range(self.size):
                if arr[i1][j1] not in (self.chars + list('0')):
                    exit('В ячейке [' + str(i1 + 1) + '][' + str(j1 + 1) + '] обнаружен недопустимый символ: ' +
                         str(arr[i1][j1]) + '. ВЫХОД.')
                if arr[i1][j1] != '0':
                    # If all correct: set char
                    self.set_num(i1, j1, arr[i1][j1])

    def show_possibles(self):
        for i1 in range(self.size):
            for j1 in range(self.size):
                string = ' ' * j1 + str(self.possibles[i1][j1]) + '\t//' + str(len(self.possibles[i1][j1]))
                print(string.expandtabs(50))

    def set_num(self, x_ins, y_ins, char_ins):
        if self.field[x_ins][y_ins] != '0' or (char_ins not in self.possibles[x_ins][y_ins]):
            self.output_puzzle()
            print(self.field)
            print(self.possibles)
            print(x_ins, y_ins, char_ins)
            exit('Головоломка содержит ошибки!')
        self.field[x_ins][y_ins] = char_ins
        self.possibles[x_ins][y_ins] = set()
        for i1 in range(self.size):
            self.possibles[i1][y_ins].discard(char_ins)
            self.possibles[x_ins][i1].discard(char_ins)
        for i1 in range(((x_ins // self.y) * self.y), ((x_ins // self.y + 1) * self.y)):
            for j1 in range(((y_ins // self.x) * self.x), ((y_ins // self.x + 1) * self.x)):
                self.possibles[i1][j1].discard(char_ins)
        # LOG:
        # if rule_ins != '':
        #     print('Set ' + str(num_ins) + ' in [' + str(x_ins + 1) + '][' + str(y_ins + 1) + '] by rule ' + rule_ins)

    def check_complete(self):
        for i1 in self.field:
            for j1 in i1:
                if j1 == '0':
                    return False
        return True

    def return_line(self):
        newline = ''
        for i1 in self.field:
            for j1 in i1:
                newline += j1
            newline += ' '
        return newline[:-1]

    def output_puzzle(self):
        print('╔' + '═' * self.x + ('╤' + '═' * self.x) * (self.y - 1) + '╗')
        for i1 in range(self.size):
            print('║', end='')
            for j1 in range(self.size):
                if self.field[i1][j1] == '0':
                    print(' ', end='')
                else:
                    print(self.field[i1][j1], end='')
                if (((j1 + 1) % self.x) == 0) and (j1 != (self.size - 1)):
                    print('│', end='')
            print('║')
            if ((i1 + 1) % self.y) == 0 and (i1 != (self.size - 1)):
                print('╟' + '─' * self.x + ('┼' + '─' * self.x) * (self.y - 1) + '╢')
        print('╚' + '═' * self.x + ('╧' + '═' * self.x) * (self.y - 1) + '╝')

# line = '0001 1000 0003 2000'
# line = '1000 0020 0300 0004'
# line = '3020 0000 0000 0102'
# line = '3000 0240 0320 0004'
# puzzle = Puzzle(2, 2, list('1234'), line)

# line = '500000 002006 000042 120000 300500 000003'
# line = '000010 050604 006000 000400 405020 030000'
# line = '002065 000200 200000 000006 001000 360400'
# line = '201000 030600 000500 004000 002040 000302'
# line = '300000 060050 600020 020001 050060 000002'
# line = '020000 001050 600310 013002 030600 000030'
# line = '150004 000000 500043 340001 000000 200035'
# puzzle = Puzzle(3, 2, list('123456'), line)

# line = '000109000 085304670 096000210 000902000 700000003 000803000 048000160 073408590 000706000'
# line = '409730102 020009600 010000390 000000021 000453000 680000000 051000030 006300010 904026805'
# ˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅˅
line = '050047001 000000708 804601050 103700000 000405000 000002406 020503904 405000000 900260010'
# line = '359847001 000359748 874621359 143706000 000405100 500002406 020503904 405008000 900264010'
# Более сложная головоломка.
# Решение: 359847261 261359748 874621359 143796825 692485173 587132496 726513984 415978632 938264517
# ╔═══╤═══╤═══╗
# ║359│847│261║
# ║261│359│748║
# ║874│621│359║
# ╟───┼───┼───╢
# ║143│796│825║
# ║692│485│173║
# ║587│132│496║
# ╟───┼───┼───╢
# ║726│513│984║
# ║415│978│632║
# ║938│264│517║
# ╚═══╧═══╧═══╝
# ˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄˄
puzzle = Puzzle(3, 3, list('123456789'), line)

# line = '07900500400c 300b00000902 000370580b90 0002800a0036 000003900500 681000000000 000000000a17 00c002600000' +
# ' 9600200c8000 0170c80ba000 50600000900b 100900700850'
# puzzle = Puzzle(6, 2, list('123456789abc'), line)

# line = '2b80403050c0 007080009000 0006b0000030 902000a01000 014000800600 700095100200 00b0046a0008 003001000970' +
# ' 00050c000402 03000007a000 000c00050300 08010b030c27'
# line = '5a7b00016090 010420000057 00000000c0b0 000000607005 0500030a2600 002070090804 80b060070900 001a90800020' +
# ' 40060c000000 0b0100000000 940000025010 070580004362'
# puzzle = Puzzle(4, 3, list('123456789abc'), line)

# line = '0b00c60700500020 c056000000da0300 100a0df006048070 0d700ae000009100 503000000010b008 0a0g000070bc0e00'+
# ' d00f1002400009gc 6020eg0bdf001000 000e006g108d0b07 438000056007c00d 00g0a30d0000f080 b00c0f000000060a' +
# ' 00a500000dg00cb0 0g07d0900b203001 00c031000000g205 01000e0090c30060'
# line = 'b5030c08d2000409 000900b0a0e00030 60000510c004020b 008g009050b00000 a0060300080f000e 20b01f007000000a' +
# ' 30008000009e00d2 087d400031006005 g00700e9000d8bf0 1c005d0000030004 8000000600170c0d 5000203000f07006' +
# ' 000009040g00bd00 70c0b0010350000f 010007030d009000 f09000gd40702018'
# puzzle = Puzzle(4, 4, list('123456789abcdefg'), line)


# line = '006ce00b0400j0070f05 480000500f0c0k0dbj20 015j00c309f0db20e000 0k0g0d6108074000a009 0005009d0i0gc00e2068' +
# ' 0070060043ik010050fg k0j00f0e0080a0000004 fd00000jbh600070c000 b000jh0050k000000406 0008040c000h0700i90b' +
# ' 704h00d01000g080j000 i0a000000j0400e10007 000108000ceji00000ad e000000g060020k00301 3g0i00a0914d00f00600' +
# ' a50b700ke0901300f000 900a000h80b0fg504070 000k02bf0d30h8006c90 0h3d104070c00j0000ba 50e0g006002070083i00'
# puzzle = Puzzle(5, 4, list('123456789abcdefghijk'), line)

# Решаемая головоломка 30×30, код для Simon Tatham's SOLO:
# 6x5:a21_23_24a28a12b4_11a16a26a15c30_9c14d15_30_17_4_14_24d5_18_12_23_1_25_27_2b28a16_11_26d16a12_7d6a3a24_15_1_18_4b17b26_10c30_5_23d18_23_20_21_1a10_17b30_7b5_28_15a6_2_12_11_25e11_19_22_8_30b15a20_13_7a10_24a12_9_29_23a27a28d6_29b10d17c8b23a16_20_25_24a19_3e8_16_29a3_30_14a25a1_18a26_22_12_6_13a19_17a23a20_15_28a7b11_17a15b29_18_20a24_7_13k3a5_9c1b7a24a5a19a20_4_3_2c11_8a28_18c25a30a19_22_26a6a12_11c5a23d1_21b25_29_18_20_4_8_27_7_4a2a26c12_25d1a22_5a6_29a16_30_23b14_18a9_5_13d8_2c14_4b20_27_7_15_19a30_1c24c21a20_22a9_13_5_27a1a29c8_10b14b26c14_27f19b29a30a13_20_1a22a5a15a17_9b18_17a20a28c15_7_23_6d9_16b13b22b19a21_25_24_19a30b17b26b28_14d18_10_9_11c6a13a3_1b4_29a5a27a13a19_25_17a11a15b7f20_10c12b11b24_20c21a3a6_2_23_27a17_26a22c22c6_19a17_23_12_14_21b18_20c4_5d25_24_16a1_26b14_11_16a8_28a29_15a23d27_30c4a13a12_2_20_5_18_8_1_7_21b29_27d19a17c12_2a24a9_30_6a22a20c11_2a5_22c6_13_16_12a26a28a8a27b4c30_16a19k21_23_28a20_26_1b7a8_27b17a27_12_26a6a25_7a20_3_24_2_29a9_1a16a18_15_21a28_23_19e4_10a11_19_18_3a22b8c6d14b30_28d23a28a20_21_8_14a27_15a19_24_1a26b11_22_18_13_9e28_1_18_25_13a14_19_7b6_15b23_12a3_30_9_24_20d21_3_13c12_22b11b24_9_28_10_25a18a14d27_26a29d9_6_27a24b26_23_2_12_17_5_14_11d21_13_8_7_10_1d11c9_3c17a25a27a21_16b2a10a15_19_22a
# line = '0lno0s0c004b0g0q0f000u9000e000 0fuh4eo00005icn1pr200s0gbq0000 g0c700006030of1i400h00qa000u5n' +
# ' 0000inkl10ah00u7005sf062cbp000 00bjm8u00f0kd70ao0c9tn0r0s0000 6t00a0000h000800n0gkpo0j300000' +
# ' 8gt03ue0p01i0qmc6d0jh0n0kfs070 0bh0f00tik0o7d0000000000030590 0010070o050j0k432000b80si000p0' +
# ' u0jmq060cb00050n00001l00ptik48 r74020q000cp000010m506t0gun00e i095d000082000e400kr7fj0u1000o' +
# ' 000l0km09d5r010t0008a00e00q000 er000000j00t0u0dk10m050f0h900i h0k0s000f7n600009g00d00m00j0lp' +
# ' oj0u00h00q00se0000ia9b00060d03 1004t050r0d0jph0b0f007000000ka 000c00b00ok000l03062nr0hq0m000' +
# ' m0006j0hncel00ik000450000pog01 q00ebg08s0tf0n0000ru00040d0c2k 5i817l00tr0000j0h000c20o09u60m' +
# ' 0k000b205m0006dgc0q0s080r00400 0ug0j00000000000lns0kq100708r0 0h0rcq060p70k3o2t0910g0ifl0snj' +
# ' 000004a0bji30m00800060000e00us 0000n0s0kl8e0rf0jo10q00bmid900 000s1ipd0ej7006f00nc03u9ok0000' +
# ' l3d000cm00b00o9sap0i0e0000rq0t 000096r0o00qn2ch5eb0000ld87a10 000b00093000h0p0r0lg0020a0fjm0'
# puzzle = Puzzle(5, 6, list('123456789abcdefghijklmnopqrstu'), line)

print('Головоломка:')
puzzle.output_puzzle()
field_test = []
possibles_test = []
while not puzzle.check_complete():
    if puzzle.field != field_test:  # or puzzle.possibles != possibles_test:
        field_test = copy.deepcopy(puzzle.field)
        for i in range(puzzle.size):
            for j in range(puzzle.size):
                for c in puzzle.possibles[i][j]:
                    # Check: only one possible char in cell?
                    if len(puzzle.possibles[i][j]) == 1:
                        puzzle.set_num(i, j, c)  # , r='one char')
                        break
                    # Check: only one possible place for char in string?
                    b = False
                    for l in range(puzzle.size):
                        if l != j:
                            b = b or (c in puzzle.possibles[i][l])
                    if not b:
                        puzzle.set_num(i, j, c)  # , r='string')
                        break
                    # Check: only one possible place for char in column?
                    b = False
                    for l in range(puzzle.size):
                        if l != i:
                            b = b or (c in puzzle.possibles[l][j])
                    if not b:
                        puzzle.set_num(i, j, c)  # , r='column')
                        break
                    # Check: only one possible place for char in area x*y?
                    b = False
                    for l in range(((i // puzzle.y) * puzzle.y), ((i // puzzle.y + 1) * puzzle.y)):
                        for m in range(((j // puzzle.x) * puzzle.x), ((j // puzzle.x + 1) * puzzle.x)):
                            if l != i or j != m:
                                b = b or (c in puzzle.possibles[l][m])
                    if not b:
                        puzzle.set_num(i, j, c)  # , r='area')
                        break
    else:
        possibles_test = copy.deepcopy(puzzle.possibles)
        # Removing possibles without setting char in one cell will be here.
        if possibles_test == puzzle.possibles:
            break
        else:
            continue
if puzzle.check_complete():
    print('Головоломка решена! Ответ:')
    puzzle.output_puzzle()
else:
    print('Решить головоломку не получилось, вот, что получилось найти:')
    puzzle.output_puzzle()
    # puzzle.show_possibles()
