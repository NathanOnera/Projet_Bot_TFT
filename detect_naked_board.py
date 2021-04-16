from PIL import Image
import numpy as np
import math
import cv2 as cv

##im1 = Image.open('data/generated_data/whole_screenshot/04162021113057.jpg')
##im2 = Image.open('data/generated_data/whole_screenshot/04162021113059.jpg')
##im3 = Image.open('data/generated_data/whole_screenshot/04162021113103.jpg')
##im4 = Image.open('data/generated_data/whole_screenshot/04162021113106.jpg')

fn1 = '04162021113057'
fn2 = '04162021113110'
fn3 = '04162021113112'
fn4 = '04162021113140'
Resultat = np.empty((37,6))

for i in range(37):
    mat1 = np.array(Image.open('data/generated_data/hexes/'+fn1+'_'+str(i)+'.jpg'))
    mat2 = np.array(Image.open('data/generated_data/hexes/'+fn2+'_'+str(i)+'.jpg'))
    mat3 = np.array(Image.open('data/generated_data/hexes/'+fn3+'_'+str(i)+'.jpg'))
    mat4 = np.array(Image.open('data/generated_data/hexes/'+fn4+'_'+str(i)+'.jpg'))
    
       

    Resultat[i,0] = math.floor(np.mean(cv.subtract(mat1,mat2).flatten()))
    Resultat[i,1] = math.floor(np.mean(cv.subtract(mat1,mat3).flatten()))
    Resultat[i,2] = math.floor(np.mean(cv.subtract(mat1,mat4).flatten()))
    Resultat[i,3] = math.floor(np.mean(cv.subtract(mat2,mat3).flatten()))
    Resultat[i,4] = math.floor(np.mean(cv.subtract(mat2,mat4).flatten()))
    Resultat[i,5] = math.floor(np.mean(cv.subtract(mat3,mat4).flatten()))

print(Resultat)
##Image.fromarray(diff1).show()
##Image.fromarray(diff2).show()
##Image.fromarray(diff3).show()
##Image.fromarray(diff4).show()
##Image.fromarray(diff5).show()
##Image.fromarray(diff6).show()

##mat1 = np.array(im1)*1.0
##mat2 = np.array(im2)*1.0
##mat3 = np.array(im3)*1.0
##mat4 = np.array(im4)*1.0

####diff = math.floor(mat1-mat2)
##
##im_diff = Image.fromarray(diff)
##im_diff.show()
