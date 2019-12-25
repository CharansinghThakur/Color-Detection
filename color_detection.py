# Importing Packages
import cv2
import pandas as pd
import numpy as np
import argparse

# Taking input from command Line
arg = argparse.ArgumentParser()
arg.add_argument('-i', '--image', required= True, help= 'Image Path')
args = vars(arg.parse_args())
img_path = args['image']

# Reading the image
img = cv2.imread(img_path)

# Variable Declaration
clicked = False
r = g = b = xpos = ypos = 0

# Taking colors data as input using Pandas
index = ['colors', 'color-names', 'hex-value', 'R-value', 'G-value', 'B-value'] 
df = pd.read_csv('colors.csv', names = index, header = None)

# Function for selecting color of selected point by double clicking the left button of mouse
def selectColor(event, x, y , flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos,clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)

# Taking a window to display an Image
cv2.namedWindow('image')

# Callback function for mouse events
cv2.setMouseCallback('image',selectColor)

# Function for getting color name of selected area
def getColorName(R,G,B):
    minimum = 10000

    #  calculate a distance(d) which tells us how close we are to color and choose the one having minimum distance.
    for i in range(len(df)):
        d = abs(R-int(df.loc[i,'R-value']))+abs(G-int(df.loc[i,'G-value']))+abs(B-int(df.loc[i,'B-value']))
        if d<=minimum:
            minimum = d
            colorName = df.loc[i,"color-names"]
    return colorName

# Updates the color name whenever the double click occurs
while(1):

    # We shown the image window
    cv2.imshow('image',img)
    if(clicked):
        cv2.rectangle(img,(20,20),(750,60),(b,g,r),-1)
        text = getColorName(r,g,b)
        cv2.putText(img, text, (50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)

        if(r+g+b>=600):
            cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
        
        clicked = False

    # Exits when the user presses the 'Esc' button
    if cv2.waitKey(20) & 0xFF ==27:
        break


# Clears all the windows       
cv2.destroyAllWindows()




