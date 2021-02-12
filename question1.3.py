#A partir de um código da cadeia de um dos números, desenhe o número correspondente ao código
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from collections import Counter

dim = (300,300)
ChainCode = []
TamanhoSinal = []
tamanhoImcolor = 8
cont = 0
imcolorCont = 1
path = "./EIN"

def rec(imcolor, point_p, value):
    if value==0:
        imcolor[point_p[0], point_p[1]] = 255
        return (point_p[0]-1, point_p[1])

    elif value==1:
        imcolor[point_p[0], point_p[1]] = 255
        return (point_p[0], point_p[1]+1)

    elif value==2:
        imcolor[point_p[0], point_p[1]] = 255
        return (point_p[0]+1, point_p[1])

    elif value==3:
        imcolor[point_p[0], point_p[1]] = 255
        return (point_p[0], point_p[1]-1)

    else:
        return point_p

def verify(imcolor, point, conec):
    global cont
    if conec == 4:
        if imcolor[point[0]-1, point[1]] == 255:
            imcolor[point[0]-1, point[1]] = 0
            ChainCode.append(0)
            TamanhoSinal.append(cont)
            cont += 1
            return (point[0]-1, point[1])
        elif imcolor[point[0], point[1]+1] == 255:
                imcolor[point[0], point[1]+1] = 0
                ChainCode.append(1)
                TamanhoSinal.append(cont)
                cont += 1
                return (point[0], point[1]+1)
        elif imcolor[point[0]+1, point[1]] == 255:
                imcolor[point[0]+1, point[1]] = 0
                ChainCode.append(2)
                TamanhoSinal.append(cont)
                cont += 1
                return (point[0]+1, point[1])
        elif imcolor[point[0], point[1]-1] == 255:
                imcolor[point[0], point[1]-1] = 0
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
    tamanhoImcolor = len(f)
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

        #cv2.imshow('Image', imcolorNew)
        #cv2.waitKey(0)

        max_xy = np.where(imcolorNew == 255)
        #print (np.shape(imcolorNew))

        imcolorNewRGB = np.zeros(np.shape(imcolor))
        imcolorNewRGB[:,:,0] = imcolorNewRGB[:,:,1] = imcolorNewRGB[:,:,2] = imcolorNew

        cv2.circle(imcolorNewRGB, (max_xy[1][0], max_xy[0][0]), int(3), (0,0,255), 2)
        goPoint = (max_xy[0][0], max_xy[1][0])
        point = verify(imcolorNew, goPoint, 4)

        while(point!=goPoint):
            cv2.circle(imcolorPlot, (point[1], point[0]), int(3), (0,0,255), 6)
            cv2.imshow('Image1', imcolorPlot)
            cv2.waitKey(1)

            cv2.circle(imcolorPlot, (point[1], point[0]), int(3), (0,255,255), 4)
            point = verify(imcolorNew, point, 4)
        

        fin = dict(Counter( ChainCode ))
        imcolorF = np.zeros(np.shape(imcolorPlot))
        pointF = (1, fin[1])
        point_p = pointF
        
        #imcolorF = np.zeros((int(fin[0]*1.2), int((fin[1]+fin[3])*1.2) ))

        for value in ChainCode:
            point_p = rec(imcolorF, point_p, value)
            cv2.imshow('return', imcolorF)
            cv2.waitKey(1)

        print(ChainCode)
        plt.subplot(tamanhoImcolor, 1, imcolorCont)
        plt.plot(ChainCode)
        imcolorCont += 1
        ChainCode=[]
    plt.show()