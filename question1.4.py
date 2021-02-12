#Implemente o algoritmo para ajustar o tamanho do códigoda cadeia de todos os números. Todos deverão ter o mesmo tamanho.
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

dim = (500,500)
ChainCode = []
conj_ChainCode = []
TamanhoSinal = []
cont = 0
imcolorCont = 1
path = "./EIN"

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

def norSinal(maior_sinal, menor_tam):
    maior_tam = len(maior_sinal)
    print('Maior Tamanho: ', maior_tam)
    print('Menor Tamanho: ', menor_tam)
    r = float(maior_tam/menor_tam)
    print('Razão', r)
    sinal_reduzido = []
    sinal_reduzido.append(maior_sinal[0])
    val = 0
    cont=1

    while (len(sinal_reduzido)<menor_tam):
        flag = int(r)
        val = val + int(r)
        resto = r - flag
        sinal_reduzido.append(maior_sinal[val])
    
    print(sinal_reduzido)
    return sinal_reduzido


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

        max_xy = np.where(imcolorNew == 255)
        imcolorNewRGB = np.zeros(np.shape(imcolor))
        imcolorNewRGB[:,:,0] = imcolorNewRGB[:,:,1] = imcolorNewRGB[:,:,2] = imcolorNew

        cv2.circle(imcolorNewRGB, (max_xy[1][0], max_xy[0][0]), int(3), (0,0,255), 2)
        goPoint = (max_xy[0][0], max_xy[1][0])
        point = verify(imcolorNew, goPoint, 4)

        while(point!=goPoint):
            cv2.circle(imcolorPlot, (point[1], point[0]), int(3), (0, 255, 255), 4)
            point = verify(imcolorNew, point, 4)
        
        print(ChainCode)
        conj_ChainCode.append(ChainCode)
        ChainCode = []


    menor = 99999
    for num in conj_ChainCode:
        tamNum = len(num)
        if tamNum < menor:
            menor = tamNum
    sinal_reduzidos = []
    novo_sinal = []
    for num in conj_ChainCode:
        val = len(num) - menor
        if val != 0:
            novo_sinal = norSinal(num, menor)
            sinal_reduzidos.append(novo_sinal)
        plt.subplot(tamanhoImcolor, 1, imcolorCont)
        plt.plot(novo_sinal)
        imcolorCont += 1
    plt.show()