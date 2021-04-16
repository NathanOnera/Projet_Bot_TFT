import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageOps
from PIL import ImageFilter
import numpy as np
import cmath
import math
#from scipy import convolve,gaussian_filter
from scipy.ndimage.filters import convolve,gaussian_filter


''' Ouverture de l'image '''
img = Image.open("Screenshot_201.PNG")     # Ouverture d'une image
w,h = img.size                         # Donne la taille de l'image (en nb de pixel)
print("Largeur : {} px, hauteur : {} px.".format(w,h))

model_vayne = img.crop((740,680,830,780))
mat_vayne = np.array(model_vayne).flatten()*1.0
normalized_vayne = mat_vayne/math.sqrt(np.inner(mat_vayne,mat_vayne))
resultat = []

for i in range(232):
    file_name = 'Screenshot_' + str(i) + '.PNG'
    img_comp = Image.open(file_name)
    comparaison = img_comp.crop((740,680,830,780))
    mat_comparaison = np.array(comparaison).flatten()*1.0
    normalized_comparaison = mat_comparaison/math.sqrt(np.inner(mat_comparaison,mat_comparaison))
    temp = mat_vayne - mat_comparaison
    scalar_product = np.inner(temp,temp)
#    scalar_product = np.inner(normalized_vayne,normalized_comparaison)
    print(scalar_product)
    print(i)
    resultat.append(scalar_product)
    img_comp.close()
