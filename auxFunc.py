import numpy as np
import heapq
import cv2

# assuring there's no doubles for a line 
def dupLines(heap):
    val = 0
    while (bool(heapq.nsmallest(1, heap, key = lambda x: 0))): #check if a there are multiple points for one line on a sudoku board 
        min = heapq.heappop(heap)
        print (min)
        if(not bool(heapq.nsmallest(1, heap, key = lambda x: 0))): val += 1 #if there is only one value left 
        elif(heap[0] - min >= 10): val += 1 

        return val



# cut sudoku board into 81 boxes 
def numBoxes(img):
    rows = np.vsplit(img, 9) #vertical split 
    boxes = []
    for r in rows:
        cols = np.hsplit(r, 9) #horizontal split 
        for box in cols:
            boxes.append(box)
    return boxes


