import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageOps
from PIL import ImageFilter
import numpy as np
import cmath
import math
#from scipy import convolve,gaussian_filter
from scipy.ndimage.filters import convolve,gaussian_filter

'''
Enseignements les plus importants à retenir :
Création de np.array
    UTILISER OBLIGATOIREMENT array2 = np.copy(array) : avec array2=array les 2 variables sont égales pour toujours
    array*1.0 : Pour manipuler des réels, en particulier pour le calcul du gradient.
Pour l'histogramme des matrices de pixel
    .flatten() : avoir l'array en une seule dimension
    histtype : accélerer le calcul
Convolution
    .convolve : se fait dans le sens non-intuitif pour toi

Concepts à creuser
    .format()
'''
## On va utiliser dans ce fichier les différentes fonctions pour faire du traitement d'image

''' Ouverture de l'image '''
img_ = Image.open("Screenshot_201.PNG")     # Ouverture d'une image
#w,h = img.size                         # Donne la taille de l'image (en nb de pixel)
#print("Largeur : {} px, hauteur : {} px.".format(w,h))

''' Transformation en matrice '''
mat_pixel = np.array(img)
plt.hist(mat_pixel.flatten(),bins = range(256),density=True,cumulative=True,histtype='step')
#plt.show(block=False)                   #block = False permet de ne pas arrêter le programme
mat = mat_pixel*1.0                 #Ici, on travaille plutôt avec une matrice qui va représenter les pixels. Le *1.0 permet de travailler avec des réels plutôt qu'avec des entiers [0,255]
#print(mat)                              # Afficher la matrice dans le prompt
#x = 100
#y = 100
#p_val = img.getpixel((x,y))                    # Donne la valeur du pixel (x,y)
#print("Valeur du pixel situé en ({},{}) : {}".format(x,y,p_val))

mat = gaussian_filter(mat,1)            #Filtrage gaussien pour réduire le bruit

 
''' Calcul du gradient '''
HX = np.array([[-1/8,0,1/8],[-2/8,0,2/8],[-1/8,0,1/8]])     # Matrices de convolution pour calculer la dérivée discrète
HY = np.array([[-1/8,-2/8,-1/8],[0,0,0],[1/8,2/8,1/8]])

deriveX = convolve(mat,HX)              # Calcul du produit de convolution, donne le gradient selon X et Y
deriveY = convolve(mat,HY)
Grad = deriveX + deriveY*1j             # Matrice gradient qui utilise les complexes (*1j) pour avoir 2 dimensions

G = np.absolute(Grad)                   # Partie absolue du gradient
Theta = np.angle(Grad)                  # Définition de l'angle

'''Post traitement du gradient'''
img_G = Image.fromarray(G).convert('L')         # On transforme la matrice du gradient en image pour la visualiser
mat_G = np.array(img_G)

img_G_ = ImageOps.autocontrast(img_G,cutoff=1)           # On travaille sur le contraste pour avoir une meilleure image : le gradient donne des pixels dont la luminosité reste dans un inverval, on l'étend avec cette fonction à l'interval [0 255] pour plus de visibilité
mat_G_ = np.array(img_G_)

#plt.hist(mat_G.flatten(),bins = range(256),density=True,cumulative=True,histtype='step')
#plt.hist(mat_G_.flatten(),bins = range(256),density=True,cumulative=True,histtype='step')

G_seuil = np.copy(mat_G_)
s = G_seuil.shape
seuil = 50
for i in range(s[0]):
    for j in range(s[1]):
        if G_seuil[i][j] < seuil:
            G_seuil[i][j] = 0.0
Image_Gradient_Seuil = Image.fromarray(G_seuil)

'''img.show()
img_G_.show()
Image_Gradient_Seuil.show()'''

'''Elimination des non-maxima'''
# On définit une fonction d'interpolation cf https://www.f-legrand.fr/scidoc/docmml/image/filtrage/bords/bords.html
def interpolation(array,x,y):
    s = array.shape
    i = math.floor(x)
    j = math.floor(y)
    t = x-i
    u = y-j
    u1 = 1.0-u
    t1 = 1.0-t
    if j==s[0]-1:
        if i==s[1]-1:
            return array[j][i]
        return t*array[j][i]+t1*array[j+1][i]
    if i==s[1]-1:
        return u*array[j][i]+u1*array[j][i+1]
    return t1*u1*array[j][i]+t*u1*array[j][i+1]+\
           t*u*array[j+1][i+1]+t1*u*array[j+1][i]
# On boucle sur l'ensemble des pixels de l'image pour retirer les gradient qui ne sont pas des extrema locaux

G_Sans_Extrema = np.copy(G_seuil)
s = G_Sans_Extrema.shape
for i in range(1,s[1]-1):
    for j in range(1,s[0]-1):
        if G_seuil[j][i]!=0:
            cos = math.cos(Theta[j][i])
            sin = math.sin(Theta[j][i])
            g1 = interpolation(G_seuil,i+cos,j+sin)
            g2 = interpolation(G_seuil,i-cos,j-sin)
            if (G_seuil[j][i]<g1) or (G_seuil[j][i]<g2):
                G_Sans_Extrema[j][i] = 0.0

Image_Sans_Extrema = Image.fromarray(G_Sans_Extrema)

# Autre méthode : approximation de l'angle Theta

G_Sans_Extrema_2 = np.copy(G_seuil)
pi = math.pi
a = np.zeros(4)
a[0] = pi/8
for k in range(1,4):
    a[k] = a[k-1]+pi/4
for j in range(1,s[0]-1):
    for i in range(1,s[1]-1):
        if G_seuil[j][i]!=0:
            b = Theta[j][i]
            if b>0:
                if (b<a[0]) or (b>a[3]):
                    g1 = G_seuil[j][i+1]
                    g2 = G_seuil[j][i+1]
                elif (b<a[1]):
                    g1 = G_seuil[j+1][i+1]
                    g2 = G_seuil[j-1][i-1]
                elif (b<a[2]):
                    g1 = G_seuil[j+1][i]
                    g2 = G_seuil[j-1][i]
                else:
                    g1 = G_seuil[j+1][i-1]
                    g2 = G_seuil[j-1][i+1]
            elif b<0:
                if (b<-a[3]):
                    g1 = G_seuil[j][i+1]
                    g2 = G_seuil[j][i-1]
                elif (b<-a[2]):
                    g1 = G_seuil[j-1][i-1]
                    g2 = G[j+1][i+1]
                elif (b<-a[1]):
                    g1 = G_seuil[j-1][i]
                    g2 = G_seuil[j+1][i]
                elif (b<-a[0]):
                    g1 = G_seuil[j-1][i+1]
                    g2 = G_seuil[j+1][i-1]
                else:
                    g1 = G[j][i+1]
                    g2 = G[j][i-1]
            if (G_seuil[j][i]<g1) or (G_seuil[j][i]<g2):
                G_Sans_Extrema_2[j][i] = 0.0

Image_Sans_Extrema_2 = Image.fromarray(G_Sans_Extrema_2)

# Binarisation
Gfinal = np.copy(G_Sans_Extrema_2)
seuil = 150
for j in range(s[0]):
    for i in range(s[1]):
        if Gfinal[j][i]<seuil:
            Gfinal[j][i] = 0.0
        else:
            Gfinal[j][i] = 255.0
            
Image_Binarisee = Image.fromarray(Gfinal)


img.show()
img_G_.show()
Image_Gradient_Seuil.show()
Image_Sans_Extrema.show()
Image_Sans_Extrema_2.show()
Image_Binarisee.show()


'''

'''
                     



'''

'''




'''
Image.fromarray(G).convert('L').show()
'''

'''
############### Filtre flou
noise = np.random.normal(0,7,mat.shape)

img_bruit = Image.fromarray(mat+noise).convert('L')
img.show()
img_bruit.show()
img_bruit.filter(ImageFilter.BoxBlur(1)).show()
img2 = img.copy()

n,m = img.size
for i in range(n-2):
    for j in range(m-2):
        value = (img.getpixel((i+1,j+1)) + img.getpixel((i,j+1)) + img.getpixel((i+2,j+1)) + img.getpixel((i+1,j+2)) + img.getpixel((i+1,j)) + img.getpixel((i,j)) + img.getpixel((i+2,j+2)) + img.getpixel((i,j+2)) + img.getpixel((i+2,j)))/9
        img2.putpixel((i+1,j+1),math.floor(value))
img2.show()
'''


'''

n,bins,patches = plt.hist(mat.flatten(),bins = range(256),density=True,cumulative=True)
#plt.show()

img_cor = ImageOps.equalize(img)
img_cor.show()
mat_cor = np.array(img_cor)

n,bins,patches = plt.hist(mat_cor.flatten(),bins = range(256),density=True,cumulative=True)
#plt.show()

img_cor.rotate(45).show()
'''

