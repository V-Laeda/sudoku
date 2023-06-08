#!/usr/bin/env python3
# coding=utf-8
import task
from copy import deepcopy

# TODO: Translate to lingua franca by PEP8 (comments only)
# TODO: Add  lingua franca version of README.md
# TODO: Internationalize it
# TODO: продумать превращение содерждимого основного цикла в одну или несколько функций,
#   вызываемых из более фундаментального цикла.
# TODO: Строку нужно будет получать иначе - из файла, командной строки или интерактивно, туда же — проверку ввода.
#   (СТРОГО ЖЕЛАТЕЛЬНО — интерактивно)
# TODO: добавить исключение возможного значения без собственно простановки символа
#   (если ясно, что в некоторых клетках число стоять не может в любом случае)
# TODO: Add checking errors and valid puzzle
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
        for line in puzzle_line.split():
            arr.append(line)
        if len(arr) != self.size:
            exit(f'Неправильное количество строк: { len(arr) } вместо { self.size }! ВЫХОД.')
        for i in range(self.size):
            if len(arr[i]) != self.size:
                exit(f'В строке { i+1 } неправильное количество столбцов: { len(arr[i]) } вместо { self.size }! ВЫХОД.')
            for j in range(self.size):
                if arr[i][j] not in (self.chars + list('0')):
                    exit(f'В ячейке { i+1 }:{ j+1 } обнаружен недопустимый символ: { arr[i][j] }. ВЫХОД.')
                if arr[i][j] != '0':
                    # If all correct: set char
                    self.set_char(i, j, arr[i][j])

    def show_possibles(self):
        for i in range(self.size):
            for j in range(self.size):
                string = ' ' * j + str(self.possibles[i][j]) + '\t//' + str(len(self.possibles[i][j]))
                print(string.expandtabs(50))

    def set_char(self, x_ins, y_ins, char_ins):
        if self.field[x_ins][y_ins] != '0' or (char_ins not in self.possibles[x_ins][y_ins]):
            self.output_puzzle()
            print(self.field)
            print(self.possibles)
            print(x_ins, y_ins, char_ins)
            exit('Головоломка содержит ошибки!')
        self.field[x_ins][y_ins] = char_ins
        self.possibles[x_ins][y_ins] = set()
        for i in range(self.size):
            self.possibles[i][y_ins].discard(char_ins)
            self.possibles[x_ins][i].discard(char_ins)
        for i in range(((x_ins // self.y) * self.y), ((x_ins // self.y + 1) * self.y)):
            for j in range(((y_ins // self.x) * self.x), ((y_ins // self.x + 1) * self.x)):
                self.possibles[i][j].discard(char_ins)
        # LOG:
        # if rule_ins != '':
        #     print('Set ' + str(num_ins) + ' in [' + str(x_ins + 1) + '][' + str(y_ins + 1) + '] by rule ' + rule_ins)

    def check_complete(self):
        for i in self.field:
            for j in i:
                if j == '0':
                    return False
        return True

    def check_puzzle(self):
        # Checking for complete!
        b = False
        for i in self.field:
            for j in i:
                b = b or (j == '0')
        if not b:
            return 'Complete'
        # Checking for having possibles for all empty cells
        for i in range(self.size):
            for j in range(self.size):
                if self.field[i][j] == '0' and len(self.possibles[i][j]) == 0:
                    return 'Error_1'
        # Checking for each char set or have possibles in each string and column and area x*y
        for char in self.chars:
            for i in range(self.size):
                b1 = False
                b2 = False
                for j in range(self.size):
                    b1 = b1 or ((char in self.possibles[i][j]) or (self.field[i][j] == char))
                    b2 = b2 or ((char in self.possibles[j][i]) or (self.field[j][i] == char))
                if not b1:
                    return 'Error_2'
                if not b2:
                    return 'Error_3'
            # Checking for each char set or have possibles in each area x*y
            for i in range(self.y):
                for j in range(self.x):
                    b = False
                    for m in range(i * self.x, i * self.x + self.x):
                        for n in range(j * self.y, j * self.y + self.y):
                            b = b or ((char in self.possibles[n][m]) or (self.field[n][m] == char))
                    if not b:
                        return 'Error_4'
        return 'Normal'

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


puzzle = Puzzle(task.x_size, task.y_size, task.chars, task.puzzle_line)

print(puzzle.check_puzzle())
print('Головоломка:')
puzzle.output_puzzle()
field_test = []
possibles_test = []
while not puzzle.check_complete():
    if puzzle.field != field_test:  # or puzzle.possibles != possibles_test:
        field_test = deepcopy(puzzle.field)
        for i in range(puzzle.size):
            for j in range(puzzle.size):
                for c in puzzle.possibles[i][j]:
                    # Check: only one possible char in cell?
                    if len(puzzle.possibles[i][j]) == 1:
                        puzzle.set_char(i, j, c)  # , r='one char')
                        break
                    # Check: only one possible place for char in string?
                    b = False
                    for m in range(puzzle.size):
                        if m != j:
                            b = b or (c in puzzle.possibles[i][m])
                    if not b:
                        puzzle.set_char(i, j, c)  # , r='string')
                        break
                    # Check: only one possible place for char in column?
                    b = False
                    for m in range(puzzle.size):
                        if m != i:
                            b = b or (c in puzzle.possibles[m][j])
                    if not b:
                        puzzle.set_char(i, j, c)  # , r='column')
                        break
                    # Check: only one possible place for char in area x*y?
                    b = False
                    for m in range(((i // puzzle.y) * puzzle.y), ((i // puzzle.y + 1) * puzzle.y)):
                        for n in range(((j // puzzle.x) * puzzle.x), ((j // puzzle.x + 1) * puzzle.x)):
                            if m != i or j != n:
                                b = b or (c in puzzle.possibles[m][n])
                    if not b:
                        puzzle.set_char(i, j, c)  # , r='area')
                        break
    else:
        possibles_test = deepcopy(puzzle.possibles)
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
