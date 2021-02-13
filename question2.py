#Utilizando os extratores LBP, HU e GLCM, extraia as
#características das imagens disponibilizadas no ClassRoom (num-
#ber1.rar) e crie um arquivo contendo linha por linha as caracterís-
#ticas extraídas a fim de montar um dataset. Não precisa incluir o
#Rótulo

from skimage.feature import greycomatrix, greycoprops
from skimage.feature import local_binary_pattern

import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import csv
import time, threading

def HU_FE(imcolor):
        moments = cv2.moments(imcolor.astype(np.float64))
        return np.asarray( cv2.HuMoments(moments).flatten())

def LBP_FE(imcolor):
        lbp_imcolor = local_binary_pattern(imcolor, 256, 1, "uniform")
        hist, ret = np.histogram(lbp_imcolor.ravel(), bins=256)
        return hist

def GLCM_FE(imcolor):
        glcm = greycomatrix(imcolor, [1], [0], 256, symmetric=True, normed=True)
        xs = []
        xs.append(greycoprops(glcm, 'dissimilarity')[0, 0])
        xs.append(greycoprops(glcm, 'correlation')[0, 0])
        xs.append(greycoprops(glcm, 'homogeneity')[0, 0])
        xs.append(greycoprops(glcm, 'ASM')[0, 0])
        xs.append(greycoprops(glcm, 'energy')[0, 0])
        xs.append(greycoprops(glcm, 'correlation')[0, 0])
        return np.asarray(xs);

def norImcolor(im):
    im = (im - im.min()) / (im.max() - im.min())
    final_im = (im * 255).astype(np.uint8)
    return final_im


dim = (300,300)
path = "./EIN"
mom_Hu = []
GLCM = []
hist_LBP = []
hist_GLCM = []
hist_HU = []
LBP = []
eps = 1e-7

for r, d, f in os.walk(path):
    
    for filename in f:
        imcolor = cv2.imread(os.path.join(path, filename), 0)
        imcolor = cv2.resize(imcolor, dim, interpolation=cv2.INTER_AREA)

        hist_HU = HU_FE(imcolor)
        hist = hist_HU.astype('float')
        imcolor_HU = [item for item in list(hist)]
        mom_Hu.append(imcolor_HU)

        hist_GLCM = GLCM_FE(imcolor)
        GLCM.append(hist_GLCM)

        hist_LBP =LBP_FE(imcolor)
        hist2 = hist_LBP.astype('float')
        hist2 /= (hist2.sum() + eps)

        imcolor_lbp = [item for item in list(hist2)]

        LBP.append(imcolor_lbp)

    print('Salvando arquivo LBP')
    with open ('LBP' + '.csv', 'w') as outfileLBP:
        writer = csv.writer(outfileLBP)
        writer.writerows(GLCM)

    print('Salvando arquivo GLCM')
    with open('GLCM' + '.csv', 'w') as outfileGLCM:
        writer = csv.writer(outfileGLCM)
        writer.writerows(GLCM)

    print('Salvando arquivo HU')
    with open('HU' + '.csv', 'w') as outfileHU:
        writer = csv.writer(outfileHU)
        writer.writerows(mom_Hu)
