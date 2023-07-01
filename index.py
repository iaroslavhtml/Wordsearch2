#!/usr/bin/env python3
# vim:sw=4:ts=4:et:
#
# partially based on https://www.tutorialspoint.com/word-search-in-python

import sys
import string
import random

DEBUG = False

GRID_EMPTY_CHAR = u"\u00B7"

DEFAULT_WIDTH = 10
DEFAULT_HEIGHT = 10
DEFAULT_MAY_REVERSE = True

class WordSearch(object):
    width = DEFAULT_WIDTH
    height = DEFAULT_HEIGHT
    may_reverse = DEFAULT_MAY_REVERSE

    def __init__(self, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, may_reverse=DEFAULT_MAY_REVERSE):
        self.width = width
        self.height = height
        self.may_reverse = may_reverse

    def make_grid(self):
        return [
            [GRID_EMPTY_CHAR for i in range(self.width)]
            for j in range(self.height)
        ]

    def randomize_grid(self, grid):
        for i in range(self.height):
            for j in range(self.width):
                if grid[i][j] == GRID_EMPTY_CHAR:
                    grid[i][j] = random.choice(string.ascii_uppercase)

    def exist(self, board, word, res_board=None, direction='default'):
        n = len(board)
        m = len(board[0])
        for i in range(n):
            for j in range(m):
                if word[0] == board[i][j]:
                    if self.find(board, word, i, j, res_board=res_board, direction=direction):
                        return True
        return False

    def find(self, board, word, row, col, i=0, direction='default', res_board=None):
        if DEBUG:
            print(f'find called: word={word} row={row} col={col} i={i}')

        if i == len(word):
            return True

        if row >= len(board) or row < 0 or col >= len(board[0]) or col < 0 or word[i] != board[row][col]:
            return False

        board[row][col] = '*'

        if direction == 'default':
            res = (
                self.find(board, word, row+1, col, i+1, res_board=res_board) or
                self.find(board, word, row-1, col, i+1, res_board=res_board) or
                self.find(board, word, row, col+1, i+1, res_board=res_board) or
                self.find(board, word, row, col-1, i+1, res_board=res_board)
             )

        elif direction == 'horizontal':
            res = (
                self.find(board, word, row, col+1, i+1, res_board=res_board, direction=direction) or
                self.find(board, word, row, col-1, i+1, res_board=res_board, direction=direction)
            )

        elif direction == 'vertical':
            res = (
                self.find(board, word, row+1, col, i+1, res_board=res_board, direction=direction) or
                self.find(board, word, row-1, col, i+1, res_board=res_board, direction=direction)
            )


        elif direction == 'diagonal_cross1':
            res = (
                self.find(board, word, row+1, col+1, i+1, res_board=res_board, direction=direction) or
                self.find(board, word, row-1, col-1, i+1, res_board=res_board, direction=direction)
            )

        elif direction == 'diagonal_cross2':
            res = (
                self.find(board, word, row+1, col-1, i+1, res_board=res_board, direction=direction) or
                self.find(board, word, row-1, col+1, i+1, res_board=res_board, direction=direction)
            )

        board[row][col] = word[i]

        if res and res_board:
            res_board[row][col] = word[i]

        return res

    def print_board(self, board):
        for row in board:
            print(' '.join(row))

    def place_word(self, word, grid):
        if self.may_reverse:
            word = random.choice([word, word[::-1]])

        choices = []
        wordlen = len(word)
        if wordlen <= self.width:
            choices.append([1,0])   # horizontal

        if wordlen <= self.height:
            choices.append([0,1])   # vertical

        if wordlen <= self.height and wordlen <= self.width:
            choices.append([1,1])   # horizontal

        if len(choices) == 0:
            raise Exception(f'The word "{word}" is too long to place')

        direction = random.choice(choices)

        if DEBUG:
            print(f'Placing {word} in direction {direction}...')

        xstart = self.width if direction[0] == 0 else self.width - len(word)
        ystart = self.height if direction[1] == 0 else self.height - len(word)

        if DEBUG:
            print(f'xstart/ystart: {xstart}/{ystart}')

        x = random.randrange(0, xstart) if xstart > 0 else 0
        y = random.randrange(0, ystart) if ystart > 0 else 0

        if DEBUG:
            print(f'x/y: {x}/{y}')

        for c in range(len(word)):
            if DEBUG:
                print(f'VERIFYING {word[c]} ({c}) in {x + direction[0]*c} / {y + direction[1]*c}')

            if grid[y + direction[1]*c][x + direction[0]*c] != GRID_EMPTY_CHAR:
                return self.place_word(word, grid)

        for c in range(len(word)):
            if DEBUG:
                print(f'PLACING {word[c]} ({c}) to {x + direction[0]*c} / {y + direction[1]*c}')
            grid[y + direction[1]*c][x + direction[0]*c] = word[c]

        return grid

if __name__ == '__main__':
    ws = WordSearch(width=10, height=10, may_reverse=False)
    grid = ws.make_grid()

    if DEBUG:
        print('Start board:')
        ws.print_board(grid)

    print("Enter words (empty string to finish):")
    words = []
    while True:
        word = input()
        if word == '':
            break
        words.append(word.upper())

    for word in words:
        if DEBUG:
            print(f"Placing word {word}")
        try:
            ws.place_word(word, grid)
        except RecursionError:
            print(f"can not place word {word}")
            ws.print_board(grid)
            sys.exit(1)

    print('Generated board:')
    ws.randomize_grid(grid)
    ws.print_board(grid)

    solved_board = ws.make_grid()
    for word in words:
        rc = (
            ws.exist(grid, word, res_board=solved_board, direction='horizontal') or
            ws.exist(grid, word, res_board=solved_board, direction='vertical') or
            ws.exist(grid, word, res_board=solved_board, direction='diagonal_cross1') or
            ws.exist(grid, word, res_board=solved_board, direction='diagonal_cross2')
        )
        print(f'Searching for {word}: {rc}')

    print('Solved board:')
    ws.print_board(solved_board)
