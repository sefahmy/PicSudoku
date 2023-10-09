import numpy as np
from IR import *
from PIL import Image, ImageDraw, ImageFont

#solve it 

#uncomment for testing 
# number = [4, 1, 5, 0, 6, 9, 0, 7, 0, 0, 0, 3, 0, 0, 1, 0, 2, 0, 0, 0, 0, 4, 0, 3, 5, 0, 0, 6, 7, 2, 1, 0, 0, 0, 0, 4, 8, 3, 0, 0, 0, 0, 0, 5, 7, 5, 0, 0, 0, 0, 8, 0, 1, 3, 2, 8, 0, 0, 0, 7, 1, 0, 6, 0, 9, 6, 0, 0, 0, 0, 4, 5, 1, 5, 0, 6, 0, 0, 8, 0, 0]

grid = []

c = 0

#convert to a matrix of matrices 
for num1 in range(0,9):
    g = []
    for num2 in range(0,9):
        x = numbers[c]
        g.append(x)
        c = c + 1
    grid.append(g) #rename numbers 

N = 9
 
# A utility function to print grid
def printing(arr):
    for i in range(N):
        for j in range(N):
            print(arr[i][j], end = " ")
        print()
 
#can a number be placed in a certain box
def isSafe(grid, row, col, num):
    for x in range(9): #already exists in the row?
        if grid[row][x] == num:
            return False
 
    for x in range(9): #already exists in column
        if grid[x][col] == num:
            return False
 
    startRow = row - row % 3 #same 3x3 box?
    startCol = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[i + startRow][j + startCol] == num:
                return False
    return True
 
#backtracking
def solveSudoku(grid, row, col):
   
    # did we reach the bottom corner? stops recursion
    if (row == N - 1 and col == N):
        return True
       
    # once done with column, next column
    if col == N:
        row += 1
        col = 0
 
    # check if this box is already filled 
    if grid[row][col] > 0:
        return solveSudoku(grid, row, col + 1)
    for num in range(1, N + 1, 1):
       
        # can the number be placed there
        if isSafe(grid, row, col, num):

            grid[row][col] = num
 
            # next num
            if solveSudoku(grid, row, col + 1):
                return True
 
        # remove num if we're wrong 
        grid[row][col] = 0
    return False
 
def newpic(): #print output image
    font = ImageFont.truetype(r'/System/Library/Fonts/MarkerFelt.ttc', 30) 

    img = Image.open("blankgrid.png")
    draw = ImageDraw.Draw(img)


    x = 21
    y = 15

    for j in range(0,9):
        txt = str(grid[j]).replace('[', '').replace(']', '').replace(',', '   ')
        draw.text((x, y), txt, font = font, fill = "red", spacing = 100)
        y = y + 47
    img.save('final.png')
    img.show()


if (solveSudoku(grid, 0, 0)):
    newpic()
else:
    print("no solution  exists ")



