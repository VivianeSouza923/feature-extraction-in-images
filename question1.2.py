#Plote uma figura com o código da cadeia de todos os números 1‘s.

import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

dim = (500,500)
ChainCode = []
TamanhoSinal = []
tamanhoImcolor = 8
cont = 0
imcolorCont = 1
path = "./EIN"

def verify(imcolor, point, conec):
    global cont
    if conec == 4:
        if imcolor[point[0]-1, point[1]] == 255:
            imcolor[point[0]-1,point[1]] = 0
            ChainCode.append(0)
            TamanhoSinal.append(cont)
            cont += 1
            return (point[0]-1, point[1])
        elif imcolor[point[0], point[1]+1] == 255:
                imcolor[point[0],point[1]+1] = 0
                ChainCode.append(1)
                TamanhoSinal.append(cont)
                cont += 1
                return (point[0], point[1]+1)
        elif imcolor[point[0]+1, point[1]] == 255:
                imcolor[point[0]+1,point[1]] = 0
                ChainCode.append(2)
                TamanhoSinal.append(cont)
                cont += 1
                return (point[0]+1, point[1])
        elif imcolor[point[0], point[1]-1] == 255:
                imcolor[point[0],point[1]-1] = 0
                ChainCode.append(3)
                TamanhoSinal.append(cont)
                cont += 1
                return (point[0], point[1]-1)
        else:
            print('none')
    else:
        return point

def norImcolor(im):
    im = (im - im.min()) / (im.max() - im.min())
    final_im = (im * 255).astype(np.uint8)
    return final_im


for r, d, f in os.walk(path):

    for filename in f:
        imcolor = cv2.imread(os.path.join(path, filename))
        imcolor = cv2.resize(imcolor, dim, interpolation=cv2.INTER_AREA)

        imcolorBina = 255 - imcolor[:,:,0]
        
        imcolorNew = np.zeros(np.shape(imcolorBina))
        kernel = np.ones((3,3), np.uint8)
        imcolorNew = norImcolor((imcolorBina>100)*1)

        imcolorCopy = np.copy(imcolorNew)
        imcolorPlot = np.zeros(np.shape(imcolor))
        imcolorPlot[:,:,0] = imcolorPlot[:,:,1] = imcolorPlot[:,:,2] = imcolorCopy

        imcolorNew = cv2.dilate(imcolorNew, kernel, iterations=1) - imcolorNew
        imcolorNew = cv2.resize(imcolorNew, dim, interpolation=cv2.INTER_AREA)

        cv2.imshow('Imagem', imcolorNew)
        cv2.waitKey(0)

        max_xy = np.where(imcolorNew == 255)
        print (np.shape(imcolorNew))

        imcolorNewRGB = np.zeros(np.shape(imcolor))
        imcolorNewRGB[:,:,0] = imcolorNewRGB[:,:,1] = imcolorNewRGB[:,:,2] = imcolorNew

        cv2.circle(imcolorNewRGB, (max_xy[1][0], max_xy[0][0]), int(3), (0,0,255), 2)
        goPoint = (max_xy[0][0], max_xy[1][0])
        point = verify(imcolorNew, goPoint, 4)

        while(point!=goPoint):
           point = verify(imcolorNew, point, 4)
        
        plt.subplot(tamanhoImcolor, 1, imcolorCont)
        plt.plot(ChainCode)
        imcolorCont += 1
        ChainCode=[]
    plt.show()