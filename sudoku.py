#!/usr/bin/env python3
# coding=utf-8
"""
    Скрипт для решения головоломок судоку.
    Головоломки импортируются как набор констант из файла tasks в виде набора констант,
    после чего создаётся класс `Puzzle` со всем необходимым для решения.
    В коде модуля - создаётся объект класса `Puzzle` и он начинает оббегаться.
    После большого общего цикла - производлится прооверка, была ли головоломка решена
    и были ли внесены изменения, в зависимости от этого либо подводится итог,
    либо гонится ещё один проход.
"""
import sys
from copy import deepcopy
from task import X_SIZE, Y_SIZE, CHARS, PUZZLE_LINE

# TODO: Translate to lingua franca by PEP8 (comments only)
# TODO: Add  lingua franca version of README.md
# TODO: Internationalize it
# TODO: продумать превращение содерждимого основного цикла в одну или несколько функций,
#   вызываемых из более фундаментального цикла.
# TODO: Строку нужно будет получать иначе - из файла, командной строки или интерактивно
#   (СТРОГО ЖЕЛАТЕЛЬНО — интерактивно)
# TODO: Реализовать проверку ввода при интерактивном вводе.
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
#       если ни одно из стартовых допущений не приведёт к решению или ошибкам,
#       то можно будет выбрать одну из этих веток
#       (желательно наиболее заполненную) для повтора ветвления).
#       Следует так же иметь в виду, что головолома может оказаться В ПРИНЦИПЕ нерешаемой,
#       хотя и будет проходить обычные проверки.


class Puzzle:
    def __init__(self, x_size, y_size, chars, puzzle_line):
        self.x_size = x_size
        self.y_size = y_size
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
            sys.exit(f'Неправильное количество строк: { len(arr) } вместо { self.size }! ВЫХОД.')
        for i in range(self.size):
            if len(arr[i]) != self.size:
                sys.exit(f"В строке {i + 1} неправильное количество столбцов: " +
                         f"{ len(arr[i]) } вместо { self.size }! ВЫХОД.")
            for j in range(self.size):
                if arr[i][j] not in (self.chars + list('0')):
                    sys.exit(f"В ячейке { i+1 }:{ j+1 } " +
                             f"обнаружен недопустимый символ: { arr[i][j] }. ВЫХОД.")
                if arr[i][j] != '0':
                    # If all correct: set char
                    self.set_char(i, j, arr[i][j])

    def show_possibles(self):
        for i in range(self.size):
            for j in range(self.size):
                string = f"{ i+1:2 } * { j+1:2 } | " + \
                    f"{ len(self.possibles[i][j]) } | { self.possibles[i][j] }"
                print(string.expandtabs(75))

    def set_char(self, x_ins, y_ins, char_ins):
        if self.field[x_ins][y_ins] != '0' or (char_ins not in self.possibles[x_ins][y_ins]):
            self.output_puzzle()
            print(self.field)
            print(self.possibles)
            print(x_ins, y_ins, char_ins)
            sys.exit('Головоломка содержит ошибки!')
        self.field[x_ins][y_ins] = char_ins
        self.possibles[x_ins][y_ins] = set()
        for i in range(self.size):
            self.possibles[i][y_ins].discard(char_ins)
            self.possibles[x_ins][i].discard(char_ins)
        for i in range((x_ins // self.y_size) * self.y_size,
                       (x_ins // self.y_size + 1) * self.y_size):
            for j in range(((y_ins // self.x_size) * self.x_size),
                           ((y_ins // self.x_size + 1) * self.x_size)):
                self.possibles[i][j].discard(char_ins)
        # LOG:
        # if rule_ins != '':
        #     print('Set {num_ins} in [{x_ins + 1}][{y_ins + 1}] by rule {rule_ins}')

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
            for i in range(self.y_size):
                for j in range(self.x_size):
                    b = False
                    for m in range(i * self.x_size, i * self.x_size + self.x_size):
                        for n in range(j * self.y_size, j * self.y_size + self.y_size):
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
        print('╔' + '═' * self.x_size + ('╤' + '═' * self.x_size) * (self.y_size - 1) + '╗')
        for i1 in range(self.size):
            print('║', end='')
            for j1 in range(self.size):
                if self.field[i1][j1] == '0':
                    print(' ', end='')
                else:
                    print(self.field[i1][j1], end='')
                if (((j1 + 1) % self.x_size) == 0) and (j1 != (self.size - 1)):
                    print('│', end='')
            print('║')
            if ((i1 + 1) % self.y_size) == 0 and (i1 != (self.size - 1)):
                print('╟' + '─' * self.x_size + ('┼' + '─' * self.x_size) * (self.y_size - 1) + '╢')
        print('╚' + '═' * self.x_size + ('╧' + '═' * self.x_size) * (self.y_size - 1) + '╝')


if __name__ == '__main__':
    puzzle = Puzzle(X_SIZE, Y_SIZE, CHARS, PUZZLE_LINE)

    print('Головоломка:')
    puzzle.output_puzzle()
    field_test = []
    possibles_test = []
    while puzzle.check_puzzle() == "Normal":
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
                        for m in range(((i // puzzle.y_size) * puzzle.y_size),
                                       ((i // puzzle.y_size + 1) * puzzle.y_size)):
                            for n in range(((j // puzzle.x_size) * puzzle.x_size),
                                           ((j // puzzle.x_size + 1) * puzzle.x_size)):
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
            continue
    if puzzle.check_puzzle() == "Complete":
        print('Головоломка решена! Ответ:')
        puzzle.output_puzzle()
    else:
        print('Решить головоломку не получилось, вот, что получилось найти:')
        puzzle.output_puzzle()
        # puzzle.show_possibles()
    input()
