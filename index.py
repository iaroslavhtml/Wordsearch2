#!/usr/bin/env python3
# vim:sw=4:ts=4:et:
#
# based on https://www.tutorialspoint.com/word-search-in-python

import string 
import random 

width = 10
height = 10 

words =  ["DOG","NO","HI","CAT", "HAMSTER"]

class Solution(object):
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
    
        direction = random.choice([[1,0], [0,1], [1,1]])
        print(f'Placing {word} in direction {direction}...')
        xstart = width if direction[0] == 0 else width - len(word) - 1
        ystart = height if direction[1] == 0 else height - len(word) - 1

        x = random.randrange(0, xstart)
        y = random.randrange(0, ystart)

        print([x, y])

        for c in range(len(word)):
            grid[x + direction[0]*c][y + direction[1]*c] = word[c]
        return grid

if __name__ == '__main__':
    ws = Solution()
    
    grid = [[random.choice(string.ascii_uppercase) for i in range(width)] 
        for j in range(height)]
    

    for word in words:
        print(f"Placing word {word}")
        ws.place_word(word, grid)

    print('Source board:')
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
            
