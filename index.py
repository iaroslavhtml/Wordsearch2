#!/usr/bin/env python3
# vim:sw=4:ts=4:et:
#
# based on https://www.tutorialspoint.com/word-search-in-python

import string
import random
import sys

width = 30
height = 30

words =  []
for i in range(4):
    words.append(input("Enter a word: ").upper())

class Solution(object):
    def make_grid(self, width=width, height=height):
        return [
            ['.' for i in range(width)]
            for j in range(height)
        ]
    def randomize_grid(self, grid):
        for i in range(height):
            for j in range(width):
                if grid[i][j] == '.':
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
        #print(f'find called: word={word} row={row} col={col} i={i}')
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

    def empty_board_from(self, board):
        res = []
        num_rows = len(board)
        num_cols = len(board[0])
        for i in range(num_rows):
            res.append([])
            for j in range(num_cols):
                res[i].append('.')
        return(res)

    def place_word(self, word, grid):
        word = random.choice([word, word[::-1]])

        choices = []
        wordlen = len(word)
        if wordlen <= width:
            choices.append([1,0])   # horizontal

        if wordlen <= height:
            choices.append([0,1])   # vertical

        if wordlen <= height and wordlen <= width:
            choices.append([1,1])   # horizontal

        if len(choices) == 0:
            raise Exception("The word is too big to place")

        direction = random.choice(choices)

        #print(f'Placing {word} in direction {direction}...')
        xstart = width if direction[0] == 0 else width - len(word)
        ystart = height if direction[1] == 0 else height - len(word)

        #print(f'xstart/ystart: {xstart}/{ystart}')

        x = random.randrange(0, xstart) if xstart > 0 else 0
        y = random.randrange(0, ystart) if ystart > 0 else 0

        #print([x, y])
        #print(f'x/y: {x}/{y}')

        for c in range(len(word)):
            #print(f'VERIFYING {word[c]} ({c}) to {x + direction[0]*c} / {y + direction[1]*c}')
            #self.print_board(grid)
            if grid[y + direction[1]*c][x + direction[0]*c] != '.':
                #raise Exception("There is alredy letter")
                return self.place_word(word, grid)

        for c in range(len(word)):
            #print(f'PLACING {word[c]} ({c}) to {x + direction[0]*c} / {y + direction[1]*c}')
            grid[y + direction[1]*c][x + direction[0]*c] = word[c]
        return grid

if __name__ == '__main__':
    ws = Solution()
    grid = ws.make_grid()

    print('Start board:')
    ws.print_board(grid)

    for word in words:
        print(f"Placing word {word}")
        try:
            ws.place_word(word, grid)
        except RecursionError:
            print(f"can not place word {word}")
            ws.print_board(grid)
            sys.exit(1)

    print('Source board:')
    ws.randomize_grid(grid)
    ws.print_board(grid)

    for word in words:
        empty_board = ws.empty_board_from(grid)
        rc = (
            ws.exist(grid, word, res_board=empty_board, direction='horizontal') or
            ws.exist(grid, word, res_board=empty_board, direction='vertical') or
            ws.exist(grid, word, res_board=empty_board, direction='diagonal_cross1') or
            ws.exist(grid, word, res_board=empty_board, direction='diagonal_cross2')
        )
        print(f'Searching for {word}: {rc}')
        if rc:
            ws.print_board(empty_board)
