#Implemente o algoritmo da cadeia, escolha um dos números e imprima o código encontrado.*/
import cv2
import numpy as np
import matplotlib as plt


dim = (300,300)

#vamos ver o grau de conectividade. 4 ou 8? boa ver. nesse caso, vamos ver 4 dimensões do xy lá. para isso, vou criar uma função chamada verify que deve receber como parametros a imagem, o ponto de referência e a conectividade em si*/
def verify(imcolor, point, conec):
    
    #beleza. se minha conec for igual a 4 (lembre-se: estou vendo 4 dim, Vivi. Então vamos só verificar 4 pontos, óbvio. código da cadeia de 4 direções), o ponto vai aparecer
    if conec == 4:
        print (point)
        #depois vou conferir se há algo no ponto abaixo (algo = 255. prof disse que se fosse booleana, 0 e 1, a imagem iria ficar preta e branca, mais ou menos assim)
        if imcolor[point[0]-1, point[1]] == 255:
            #se sim, vamos atribuir 0 a este ponto!!!!!!
            imcolor[point[0]-1,point[1]] = 0
            print('0')
            return (point[0]-1, point[1])

        #verifica segundo ponto que nem o primeiro
        elif imcolor[point[0], point[1]+1] == 255:
                imcolor[point[0],point[1]+1] = 0
                print('1')
                return (point[0], point[1]+1)

        #verificar terceito ponto que nem o segundo
        elif imcolor[point[0]+1, point[1]] == 255:
                imcolor[point[0]+1, point[1]] = 0
                print('2')
                return (point[0]+1, point[1])

        #verifica quarto ponto que nem o terceiro
        elif imcolor[point[0], point[1]-1] == 255:
                imcolor[point[0],point[1]-1] = 0
                print('3')
                return (point[0], point[1]-1)
        #se n tiver nada, taca o "none" (printar, no caso)
        else:
            print('none')
            
    else:
        return point


#bora normalizar a imagem!
def norImcolor(im):
    im = (im - im.min()) / (im.max() - im.min())
    final_im = (im * 255).astype(np.uint8)
    return final_im

#após normalizaçaão da imagem, vou lê-la e convertê-la em binário
imcolor = cv2.imread("/home/vivi/Documentos/LAPISCO-DATA-SCIENCE-IMAGE/EIN/1_1.png")
imcolor = cv2.resize(imcolor, dim, interpolation = cv2.INTER_AREA)
imcolorBina = 255 - imcolor[:,:,0]

#limiriazinado e multiplicando por 1. Após ser limiriaziada, será atribuída a imcolornew
imcolorNew = norImcolor((imcolorBina>100)*1)
#fazer a matriz de zeros, o shape de entrada será o da imagem binarizada
imcolorNew = np.zeros(np.shape(imcolorBina))
#criar a array 3x3 de 1's, do tipo inteiros (0 a 255). vamos usar na dilatação.
kernel = np.ones((3,3), np.uint8)

#plotação da imcolornew
imcolorCopy = np.copy(imcolorNew)
imcolor_plotada = np.zeros(np.shape(imcolor))
imcolor_plotada[:,:,0] = imcolor_plotada[:,:,1] = imcolor_plotada[:,:,2] = imcolorCopy


#exibição da imagem plotada 
cv2.imshow('Imagem', imcolor_plotada)
cv2.waitKey(0)

#dilatação da partezinha branca
imcolorNew = cv2.dilate(imcolorNew, kernel, iterations=1) - imcolorNew

#onde existem valores iguais a 255? Aplicando essa função vamos saber onde tem os 255, através de uma lista
max_xy = np.where(imcolorNew == 255)
print(max_xy[0][0] , max_xy[1][0])

imcolorNewRGB = np.zeros(np.shape(imcolor))
imcolorNewRGB[:,:,0] = imcolorNewRGB[:,:,1] = imcolorNewRGB[:,:,2] = imcolorNew

#botar o cícrulo na imagem. 
cv2.circle(imcolorNewRGB, (max_xy[1][0], max_xy[0][0]), int(3), (0,0,255), 2)
goPoint = (max_xy[0][0], max_xy[1][0])
point = verify(imcolorNew, goPoint, 4)

#iniciar a verificação de vizinhança

#enquanto meu ponto for DIFERENTE do meu ponto de inicio:
while(point!= goPoint):
    cv2.circle(imcolornewRGB, (point[1], point[0]), int(3), (0,0,255), 4)
    cv2.imshow('Resultado1', imcolor_plotada)
    cv2.waitKey(1)

    cv2.circle(imcolor_plotada, (point[1], point[0]), int(3), (0,255,255), 6)
    point = verify(imcolorNew, point, 4)

print('\n*************código encontrado**********************\n')
cv2.imshow('REsultado2', imcolor_plotada)
cv2.waitKey(0)
