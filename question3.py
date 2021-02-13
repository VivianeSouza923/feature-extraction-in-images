'''
Escolha um video de sua preferência com imagens reais
e sugira uma aplicação. Implemente um código com algum extrator
visto em aula para resolver essa aplicação. Algumas sugestões de
links estão disponíveis na planilha Live Cameras, disponibilizada
no ClassRoom.

'''

import cv2
import matplotlib.pyplot as plt
from skimage.feature import local_binary_pattern
import numpy as np

def LBP_FE(imcolor):
    lbp_imcolor = local_binary_pattern(imcolor, 256, 1, "uniform")
    hist, ret = np.histogram(lbp_imcolor.ravel(), bins=256)
    return hist

eps = 1e-7
captura = cv2.VideoCapture('thorinho.mp4')
cont = 0

while (1):
    ret, frame = captura.read()
    frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if(cont%12==0):
        frame3 = frame2.astype('uint8')
        hist_LBP = LBP_FE(frame3)
        hist2 = hist_LBP.astype('float')
        hist2 /= (hist2.sum() + eps)

        imcolor_lbp = [item for item in list(hist2)]
        plt.plot(imcolor_lbp)
        plt.show()
        cv2.imshow("Video do Thorinho lindo", frame2)
        k = cv2.waitKey(30) & 0xff
        cont += 1
        if k == 27:
            break
    else:
        cv2.imshow("Video do Thorinho lindo too", frame2)
        cont = cont + 1
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    plt.show(captura)
captura.release()
cv2.destroyAllWindows()