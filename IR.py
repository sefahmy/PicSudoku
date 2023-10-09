import numpy as np
import cv2
import heapq
from auxFunc import *
import keras_ocr

#doesn't work if there is an ad or the home bar 

# Load image, grayscale, median blur, sharpen image
image = cv2.imread(r'/Users/simonfahmy/Desktop/imageRec/test1.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
# Use canny edge detection
edges = cv2.Canny(gray,50,150,apertureSize=3)
 
# Apply HoughLinesP method to
# to directly obtain line end points
lines_list =[]
lines = cv2.HoughLinesP(
            edges, # Input edge image
            1, # Distance resolution in pixels
            np.pi/180, # Angle resolution in radians
            threshold=240, # Min number of votes for valid line, 240
            minLineLength=20, # Min allowed length of line
            maxLineGap=10 # Max allowed gap between line for joining them
            )
 

maxX = maxY = -2
minX = minY = 20000

#int to check if it has 9 perpendicular lines 
top = bottom = right = left = 0

topP = [] 
bottomP = [] 
rightP = []
leftP = []

heapq.heapify(topP)
heapq.heapify(bottomP)
heapq.heapify(rightP)
heapq.heapify(leftP)

# Iterate over points
for points in lines:
      # Extracted points nested in the list
    x1,y1,x2,y2=points[0]
    # Draw the lines joing the points
    # On the original image
    cv2.line(image,(x1,y1),(x2,y2),(0,255,0),2)

    #the corners of the board are always a max/min x and a max/min y
    if x1 < minX: minX = x1
    if x2 < minX: minX = x2
    if x1 > maxX: maxX = x1
    if x2 > maxX: maxX = x2

    if y1 < minY: minY = y1
    if y2 < minY: minY = y2
    if y1 > maxY: maxY = y1
    if y2 > maxY: maxY = y2


    # Maintain a simples lookup list for points
    lines_list.append([(x1,y1),(x2,y2)])
     
#value to hold corners, top left, right, bottom left. right
corners = ([(minX,maxY),(maxX,maxY), (minX,minY),(maxX,minY)])

for points in lines:
    #this function logic assumes that the sudoku board is perfectly level 
    x1,y1,x2,y2=points[0]
    if (abs(y1 - maxY) <= 10 or (abs(y2 - maxY) <= 10)): #is one of the points on the top line? 
        if (x2 == x1): heapq.heappush(topP, x2) #if the x-values are the same, then it is perp to the top
    
    if (abs(y1 - minY) <= 10 or (abs(y2 - minY) <= 10)): #is one of the points on the bottom line? 
        if (x2 == x1): heapq.heappush(bottomP, x2) #if the x-values are the same, then it is perp to the bottom
    
    if (abs(x1 - maxX) <= 10 or (abs(x2 - maxX) <= 10)): #is one of the points on the right line? 
        if (y2 == y1): heapq.heappush(rightP, y2) #if the y-values are the same, then it is perp to the right

    if (abs(x1 - minX) <= 10 or (abs(x2 - minX) <= 10)): #is one of the points on the left line? 
        if (y2 == y1): heapq.heappush(leftP, y2) #if the y-values are the same, then it is perp to the left


# Save the result image
cv2.imwrite('detectedLines.png',image)

# for number in lines_list:
    # print(number)

print(corners)

# how to make this a function which can be called, values don't work
# top and bottom are switched for some reason, but that actually doesn't matter tbh 

# checks for perpendicular lines, assuring there are no doubles, if there is 10 lines, then it works 
#top
while (bool(heapq.nsmallest(1, topP, key = lambda x: 0))): #check if a there are multiple points for one line on a sudoku board 
    min = heapq.heappop(topP)
    if(not bool(heapq.nsmallest(1, topP, key = lambda x: 0))): top += 1 #if there is only one value left 
    elif(topP[0] - min >= 10): top += 1 

#bottom
while (bool(heapq.nsmallest(1, bottomP, key = lambda x: 0))): #check if a there are multiple points for one line on a sudoku board 
    min = heapq.heappop(bottomP)
    if(not bool(heapq.nsmallest(1, bottomP, key = lambda x: 0))): bottom += 1 #if there is only one value left 
    elif(bottomP[0] - min >= 10): bottom += 1 

#right
while (bool(heapq.nsmallest(1, rightP, key = lambda x: 0))): #check if a there are multiple points for one line on a sudoku board 
    min = heapq.heappop(rightP)
    if(not bool(heapq.nsmallest(1, rightP, key = lambda x: 0))): right += 1 #if there is only one value left 
    elif(rightP[0] - min >= 10): right += 1 

#left 
while (bool(heapq.nsmallest(1, leftP, key = lambda x: 0))): #check if a there are multiple points for one line on a sudoku board 
    min = heapq.heappop(leftP)
    if(not bool(heapq.nsmallest(1, leftP, key = lambda x: 0))): left += 1 #if there is only one value left 
    elif(leftP[0] - min >= 10): left += 1 



print("top: ", top, "bottom: ", bottom, "right: ", right, "left: ", left)

# new variables to help split the boxes 

valid = False

if ((top == 10 or bottom == 10) and (left == 10 or right == 10)):
    valid = True
    
if valid: print("Valid Sudoku Board!!!")
else: print ("Invalid Sudoku Board")

# if not valid, end the program here

#adjust to be divisible by 9

divY = (maxY - minY) % 9
divX = (maxX - minX) % 9

if(divY != 0): maxY += 9 - divY
if(divX != 0): maxX += 9 - divX


croppedImage = gray[minY:maxY, minX:maxX] #height, then width, this is brute force solution, must be fixed 

cv2.imwrite('croppedImage.png', croppedImage)

(thresh, im_bw) = cv2.threshold(croppedImage, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) #make it black and white 

# cut sudoku board into 81 boxes 
boxes = numBoxes(im_bw) #boxes goes from left to right, then down once the first row is finished

for num in range(0,len(boxes)): 
    cv2.imwrite(str(num) + ".png", boxes[num])



# time for OCR! (optical character recognition)


#keras ocr 

pipeline = keras_ocr.pipeline.Pipeline()

# solution could be using pyautogui to match a screenshot to an image in the array 

numbers = []

for num in range(0,81): #all 7s are Zs, one 6 is a 0, 5 is 0
    testIM = [keras_ocr.tools.read(i) for i in [str(num) + '.png']]
    y = pipeline.recognize(testIM)
    
    if len(y[0]) <= 0 or (y[0][0][0].isdigit() == False and y[0][0][0] != 'z'): numbers.append(0) #0 means empty box 
    else: 
        value = y[0][0][0]
        if(value == "z"): numbers.append(7) #is there a way to do it better than manually??
        elif(value == "0"): numbers.append(6)
        else: numbers.append(int(value))

#solve it 



