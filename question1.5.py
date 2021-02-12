#Utilizando o Código 3, desenhe um número baseado na moda
#das cadeias geradas pelo Código 4. Adicione uma aleatoriedade para
#criar novos números a cada execução do código.

import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from collections import Counter
from random import randint

dim = (300,300)
ChainCode = []
conj_ChainCode = []
TamanhoSinal = []
cont = 0
imcolorCont = 1
path = "./EIN"

def most_frequent(list):
    occurence_count = Counter(list)
    rand = 0
    if occurence_count.most_common(1)[0][1]<=2:
        rand = randint(0,1)

    return occurence_count.most_common(1)[0][rand]

def rec(imagem, point_p, value):
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

def normalizaSinal(maior_sinal, menor_tam):
    maior_tam = len(maior_sinal)
    r = float(maior_tam/menor_tam)
    sinal_reduzido = []
    sinal_reduzido.append(maior_sinal[0])
    val = 0
    cont=1

    while (len(sinal_reduzido)<menor_tam):
        flag = int(r)
        val = val +int(r)
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
            point = verify(imcolorNew, point, 4)

        conj_ChainCode.append(ChainCode)        
        print(ChainCode)
        plt.subplot(tamanhoImcolor, 1, imcolorCont)
        plt.plot(ChainCode)
        imcolorCont += 1
        ChainCode = []

    menor = 99999
    for num in conj_ChainCode:
        tamNum = len(num)
        if tamNum < menor:
            menor = tamNum
    sinal_reduzido = []
    novo_sinal = []
    for num in conj_ChainCode:
        val = len(num) - menor
        if val != 0:
            novo_sinal = normalizaSinal(num, menor)
            sinal_reduzido.append(novo_sinal)

    imagem_recuperada = np.zeros((dim))

    pronto_in = (0,50)
    point_p = pronto_in

    sinal_reduzido = np.array(sinal_reduzido)
    print('---------------- Final ---------------')
    print(np.shape(sinal_reduzido))
    b = 0
    sinal_final = []

    for ch in range(menor):
        listch = sinal_reduzido[:,ch]

        npArray = np.array([b for elemento in listch])
        val = most_frequent(sinal_reduzido[:,ch])

        point_p = rec(imagem_recuperada, point_p, val)
        cv2.imshow('Imagem Recuperada', imagem_recuperada)
        cv2.waitKey(1)

    cv2.waitKey(0)    