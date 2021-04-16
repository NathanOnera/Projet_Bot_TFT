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
resultat_R = []
resultat_G = []
resultat_B = []
rang = 170
for i in range(rang):
    file_name = 'Screenshot_2_' + str(i) + '.PNG'
    img = Image.open(file_name)     # Ouverture d'une image
    model = img.crop((780,720,790,740))
#    model = img.crop((740,680,830,780))
#    model.show()
    mat = np.array(model)*1.0
    resultat_R.append(mat[:,:,0].flatten().mean())
    resultat_G.append(mat[:,:,1].flatten().mean())
    resultat_B.append(mat[:,:,2].flatten().mean())
    img.close()
    print(i)
plt.plot(range(rang),resultat_R,range(rang),resultat_G,range(rang),resultat_B)
plt.show(block=False)

'''
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(resultat_R,resultat_G,resultat_B,'bo')

plt.show(block=False)

    mat_G = mat[:,:,1].flatten()
    mat_B = mat[:,:,2].flatten()
    mean = [mat_R.mean(),mat_G.mean(),mat_B.mean()]
#model.show()
#mat_vayne = np.array(model_vayne).flatten()*1.0


#mean_R = 


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

'''
