# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import sys
import cv2
import collections
import numpy as np
import scipy as sc
import matplotlib.pyplot as plt

# k-means
from sklearn.cluster import KMeans

# keras
from keras.models import Sequential
from keras.layers.core import Dense,Activation
from keras.optimizers import SGD

import matplotlib.pylab as pylab
pylab.rcParams['figure.figsize'] = 16, 12 # za prikaz većih slika i plotova, zakomentarisati ako nije potrebno

#Funkcionalnost implementirana u V1
def load_image(path):
    return cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)
def image_gray(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
def image_bin(image_gs):
    ret,image_bin = cv2.threshold(image_gs, 80, 255, cv2.THRESH_BINARY)
    return image_bin
def image_bin_adaptive(image_gs):
    image_bin = cv2.adaptiveThreshold(image_gs, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 35, 10)
    return image_bin
def invert(image):
    return 255-image
def display_image(image, color= False):
    if color:
        plt.imshow(image)
    else:
        plt.imshow(image, 'gray')
def dilate(image):
    kernel = np.ones((3,3)) # strukturni element 3x3 blok
    return cv2.dilate(image, kernel, iterations=1)
def erode(image):
    kernel = np.ones((3,3)) # strukturni element 3x3 blok
    return cv2.erode(image, kernel, iterations=2)
def erode2(image):
    kernel = np.ones((3,3)) # strukturni element 3x3 blok
    return cv2.erode(image, kernel, iterations=1)
#Funkcionalnost implementirana u V2
def resize_region(region):
    resized = cv2.resize(region,(28,28), interpolation = cv2.INTER_NEAREST)
    return resized
def scale_to_range(image):
    return image / 255
def matrix_to_vector(image):
    return image.flatten()
def prepare_for_ann(regions):
    ready_for_ann = []
    for region in regions:
        ready_for_ann.append(matrix_to_vector(scale_to_range(region)))
    return ready_for_ann
def convert_output(outputs):
    return np.eye(len(outputs))
def winner(output):
    return max(enumerate(output), key=lambda x: x[1])[0]

def remove_noise(binary_image):
    ret_val = dilate(erode(binary_image))
    ret_val = invert(ret_val)
    return ret_val
global chesstable
pocetna_x_koordinata = 12
pocetna_y_koordinata = 12
sirina_kvadrata = 90







def color(region):
    xt,yt,w,h = cv2.boundingRect(region)
    number = 0
    for i in range(0, w):
        for j in range(0, h):
            number += region[i,j]
            

#    print 'Prosecno osvetljenje:', number/(w*h)
   
      
    return 1-((number/(w*h))/110)












def select_roi(image_orig, image_bin):
    '''Oznaciti regione od interesa na originalnoj slici. (ROI = regions of interest)
        Za svaki region napraviti posebnu sliku dimenzija 28 x 28. 
        Za označavanje regiona koristiti metodu cv2.boundingRect(contour).
        Kao povratnu vrednost vratiti originalnu sliku na kojoj su obeleženi regioni
        i niz slika koje predstavljaju regione sortirane po rastućoj vrednosti x ose
    '''
    img, contours, hierarchy = cv2.findContours(image_bin.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    regions = []
    props = []
    #contours_acc = []
    redni_br = 0
    broj_prihvacenih_kontura = 0
    #print 'Broj kontura:', len(contours)
    
    for contour in contours: 
        x,y,w,h = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)
        
        if area > 850 and h < 200 and w < 200:
            
            #contours_sb.append(contour)
            broj_prihvacenih_kontura = broj_prihvacenih_kontura + 1
            
            region = image_bin[y:y+h+1,x:x+w+1];
            #print 'X:', x
            
            figure_color = color(resize_region(region))
            
            #print 'Boja',figure_color
            
            broj_polja_horizontalno = 1
            broj_polja_vertikalno = 1
        
#            print 'Pozicija x :', (x)/sirina_kvadrata
            x_polje = broj_polja_horizontalno + ((x)/sirina_kvadrata)
            
#            print 'Pozicija y :', (y)/sirina_kvadrata
            y_polje = broj_polja_vertikalno + ((y)/sirina_kvadrata)
        
            props.append((x_polje, y_polje, figure_color, resize_region(region), contour ))
            cv2.rectangle(image_orig,(x,y),(x+w,y+h),(0,255,0),2)
    
    props = sorted(props)
    
    
    #print [(x_polje,y_polje, figure_color) for x_polje,y_polje,figure_color,region, contour in props]
    chesstable = [(x_polje,y_polje, figure_color) for x_polje,y_polje,figure_color,region, contour in props]

#    (x_polje,y_polje, figure_color) for x_polje,y_polje,figure_color,region, contour in props
#        chesstable.append(x_polje,y_polje, figure_color)
        
        
        
#    print 'tabele', len(chesstable)
    contour1 = [contour for x_polje, y_polje, figure_color,region, contour in props]
    regions = [region for x_polje,y_polje,figure_color,region, contour in props]
    
    return image_orig, regions, contour, chesstable
















img_train = load_image('trenira.png')
img_train_bin = remove_noise(image_bin(image_gray(img_train)))
display_image(img_train_bin)

img, contours, hierarchy = cv2.findContours(img_train_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

img = img_train.copy()
cv2.drawContours(img, contours, -1, (255,0,0), 1)
print 'broj figura', len(contours)
plt.imshow(img)










def create_ann():
    '''
    Implementirati veštačku neuronsku mrežu sa 28x28 ulaznih neurona i jednim skrivenim slojem od 128 neurona.
    Odrediti broj izlaznih neurona. Aktivaciona funkcija je sigmoid.
    '''
    ann = Sequential()
    # Postaviti slojeve neurona mreže 'ann'
    ann.add(Dense(128, input_dim=28 * 28, activation='sigmoid'))
    ann.add(Dense(6, activation='sigmoid'))
    return ann
    
def train_ann(ann, X_train, y_train):
    X_train = np.array(X_train, np.float32)
    y_train = np.array(y_train, np.float32)
   
    # definisanje parametra algoritma za obucavanje
    sgd = SGD(lr=0.01, momentum=0.9)
    ann.compile(loss='mean_squared_error', optimizer=sgd)

    # obucavanje neuronske mreze
    ann.fit(X_train, y_train, nb_epoch=500, batch_size=1, verbose = 0, shuffle=False, show_accuracy = False) 
      
    return ann











img_train = load_image('trenira.png')
img_train_bin = remove_noise(image_bin(image_gray(img_train)))
sel_img_train, shapes, contour, chesstable = select_roi(img_train.copy(), img_train_bin)

display_image(img_train_bin)

print 'Broj kontura :', len(shapes)

inputs = prepare_for_ann(shapes)
alphabet = ['K', 'P', 'N', 'R', 'Q', 'B']
outputs = convert_output(alphabet)
ann = create_ann()
ann = train_ann(ann, inputs, outputs)



def display_result(outputs, alphabet):
    '''
    Funkcija određuje koja od grupa predstavlja razmak između reči, a koja između slova, i na osnovu
    toga formira string od elemenata pronađenih sa slike.
    Args:
        outputs: niz izlaza iz neuronske mreže.
        alphabet: niz karaktera koje je potrebno prepoznati
        kmeans: obučen kmeans objekat
    Return:
        Vraća formatiran string
    '''
    elements = []

   
    for idx, output in enumerate(outputs[0:,:]):
        elem = alphabet[winner(output)]
        elements.append(elem)
        #print 'Elemenat: ', elem


    
    return elements
    


def main (filepath):
    img_test = load_image(filepath)
    img_test_bin = remove_noise(image_bin(image_gray(img_test)))

    #display_image(img_test_bin)

    img, contours, hierarchy = cv2.findContours(img_test_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #print chesstable
    
    img = img_test.copy()
    cv2.drawContours(img, contours, -1, (255,0,0), 1)
    print 'broj figura', len(contours)
    #plt.imshow(img)








    img_test = load_image(filepath)
    img_test_bin = remove_noise(image_bin(image_gray(img_test)))

    ret_val = erode2(img_test_bin )
    display_image(ret_val)
    #display_image(img_test_bin)
    sel_img_test, shapes, contour, chesstable = select_roi(img_test.copy(), ret_val)
    print 'Konture', len(chesstable)
    print chesstable


    inputs = prepare_for_ann(shapes)
    results = ann.predict(np.array(inputs, np.float32))
    figures = display_result(results, alphabet)
    
    print figures
    return chesstable, figures

if __name__ == "__main__":
    main(sys.argv[1])






