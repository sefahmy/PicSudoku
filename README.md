# PicSudoku


py-opencv=4.8.0 
kerasocr
tensorflow v2.13.0

• Developed a web app where users can upload an image of a sudoku board and the algorithm would determine if it is a valid board then solve it 
• Utilized OpenCV line detection to detect patterns and that indicate a Sudoku board is present     
• Implemented KerasOCR to process an image, then detect where the number and spaces are 
• Saved 5 seconds of runtime with image processing and proper complex data structure usage 
• Solves the board using a backtracking algorithm
• Script writes the final answer onto a blank image utilizing Python Imaging Library   

Development
• IR.py: imports image and preprocesses it then finds the numbers 
• solver.py: solves the board then outputs final board 

![detectedLines](https://github.com/sefahmy/PicSudoku/assets/115515604/70792979-c8a4-4e41-b67d-89d18232ef4c)

![croppedImage](https://github.com/sefahmy/PicSudoku/assets/115515604/3168ff41-2189-47a9-8cff-883eebbdbb8b)

![final](https://github.com/sefahmy/PicSudoku/assets/115515604/e352b725-4f38-481c-a08b-6c35952d0807)
