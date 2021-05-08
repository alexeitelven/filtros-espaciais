# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 22:37:47 2021

@author: Alex e Eduardo Eitelven

Os filtros espaciais implementados:

Filtro de média (borramento)
Filtro Gaussiano (borramento)
Filtro de mediana
Filtro de Sobel
Filtro Laplaciano
Filtro de Canny

--- Como usar? ---
1- Selecionar uma imagem.
2- clicar em "Carregar Imagem".
3- Selecionar o filtro desejado.

Irá ser mostrado na tela do programa a imagem original a esquerda e o filtro aplicado a direita.

"""


import io
import os
import PySimpleGUI as sg
from PIL import Image
import cv2 as cv2
from win32api import GetSystemMetrics
import numpy as np


#print("Width =", GetSystemMetrics(0))
#print("Height =", GetSystemMetrics(1))
larguraTela = GetSystemMetrics(0)
alturaTela = GetSystemMetrics(1)


#Tipos de arquivos que podemos abrir
file_types = [("JPEG (*.jpg)", "*.jpg"),
              ("All files (*.*)", "*.*")]

def atualizaImagem(imagem):
    #Cria uma imagem temporária para mostrar a imagem editada na tela do programa
    cv2.imwrite("temp.png",imagem) 
    image = Image.open("temp.png")
    image.thumbnail((larguraTela, alturaTela)) 
    bio = io.BytesIO()
    image.save(bio, format="PNG") 
    return bio


#-----------------------------------------------------------------------------
def main():

    #sg.theme('Gray')
    layout = [      
        [
            sg.Text("Caminho do Arquivo"),
            sg.Input(size=(25, 1), key="Arquivo"),
            sg.FileBrowse(file_types=file_types),
            sg.Button("Carregar Imagem"),
        ],
        [
            sg.Text("Filtros Espaciais"),
            sg.Button("Filtro de média"),
            sg.Button("Filtro Gaussiano"),
            sg.Button("Filtro de mediana"),
            sg.Button("Filtro de Sobel X"),
            sg.Button("Filtro de Sobel Y"),
            sg.Button("Filtro de Laplacitano"),
            sg.Button("Filtro de Canny"),
        ],
        [
            sg.Text("Transformações Geometricas"),
            sg.Button("Ajuste Escala"),
            sg.Button("Perspectiva"),
            sg.Button("Rotacao"),
            sg.Button("Translação"),
        ],
          [
            sg.Text("Espelhamento"),  
            sg.Button("Flip Horizontal"),
            sg.Button("Flip Vertical"),
            sg.Button("Flip Horizontal e Vertical"),
        ],
        [
            sg.Image(key="-imgOriginal-"),
            sg.Image(key="-imgEditada-") 
        ],
    ]
    
    window = sg.Window("Filtros Espaciais",layout,finalize=True,resizable=True)
    window.maximize()
    
    
    while True:
        # enquanto o programa estiver aberto verifica a ocorrencia dos eventos
        event, values = window.read()
        
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        
        if event == "Carregar Imagem":
            filename = values["Arquivo"]
            if os.path.exists(filename):
                image = Image.open(values["Arquivo"])
                image.thumbnail((larguraTela/2, alturaTela/2))
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                window["-imgOriginal-"].update(data=bio.getvalue())
                window["-imgEditada-"].update(data=bio.getvalue())
        # -- FILTROS ESPACIAIS
        if event == "Filtro de média":
            img = cv2.imread(values["Arquivo"])   
            imgGaussiano=cv2.blur(img, (3,3)) #Esse é o Filtro de média?
            bio = atualizaImagem(imgGaussiano)
            window["-imgEditada-"].update(data=bio.getvalue())

        if event == "Filtro Gaussiano": 
            img = cv2.imread(values["Arquivo"])   
            imgGaussiano=cv2.GaussianBlur(img, (5,5),50)
            bio = atualizaImagem(imgGaussiano)
            window["-imgEditada-"].update(data=bio.getvalue())
    
        if event == "Filtro de mediana": 
            img = cv2.imread(values["Arquivo"])       
            imgMediana=cv2.medianBlur(img, 15)
            bio = atualizaImagem(imgMediana)
            window["-imgEditada-"].update(data=bio.getvalue())
        
        if event == "Filtro de Sobel X": 
            img = cv2.imread(values["Arquivo"])             
            sobelX=cv2.Sobel(img, cv2.CV_8U,  0, 1, ksize=3)
            bio = atualizaImagem(sobelX)
            window["-imgEditada-"].update(data=bio.getvalue())
        
        if event == "Filtro de Sobel Y": 
            img = cv2.imread(values["Arquivo"])             
            sobelY=cv2.Sobel(img, cv2.CV_8U,  1, 0, ksize=3)
            bio = atualizaImagem(sobelY)
            window["-imgEditada-"].update(data=bio.getvalue())
          
        if event == "Filtro de Laplacitano": 
            img = cv2.imread(values["Arquivo"])   
            imgLaplacitano=cv2.Laplacian(img, cv2.CV_8U)
            bio = atualizaImagem(imgLaplacitano)
            window["-imgEditada-"].update(data=bio.getvalue())
    
        if event == "Filtro de Canny": 
            img = cv2.imread(values["Arquivo"])   
            imgCanny=cv2.Canny(img,100,200)
            bio = atualizaImagem(imgCanny)
            window["-imgEditada-"].update(data=bio.getvalue())
       
        # -- FILTROS GEOMETRICOS    
       
        if event == "Ajuste Escala": 
            img = cv2.imread(values["Arquivo"])   
            imgEscala=cv2.resize(img, None, fx=1.5,fy=1.5, 
                           interpolation = cv2.INTER_CUBIC)
            bio = atualizaImagem(imgEscala)
            window["-imgEditada-"].update(data=bio.getvalue())
         
        if event == "Perspectiva": 
            img = cv2.imread(values["Arquivo"])   
            pontosiniciais=np.float32([[189,87],[459,84],[192,373],[484,372]])
            pontofinais=np.float32([[0,0],[500,0],[0,500],[500,500]])
            matriz=cv2.getPerspectiveTransform(pontosiniciais,pontofinais)
            imgPerspectiva = cv2.warpPerspective(img, matriz,(500,500))
            bio = atualizaImagem(imgPerspectiva)
            window["-imgEditada-"].update(data=bio.getvalue())
       
        if event == "Rotacao": 
            img = cv2.imread(values["Arquivo"])   
            totallinhas, totalcolunas = img.shape[:2]
            matriz=cv2.getRotationMatrix2D((totallinhas/2, totalcolunas/2),23,1)
            iimagemRotacionada = cv2.warpAffine(img, matriz, (totallinhas, totalcolunas))
            bio = atualizaImagem(iimagemRotacionada)
            window["-imgEditada-"].update(data=bio.getvalue())
       
        if event == "Translação": 
            img = cv2.imread(values["Arquivo"])   
            linhas, colunas = img.shape[:2]
            matriz=np.float32([[1,0,400],[0,1,400]])
            imgDeslocada=cv2.warpAffine(img, matriz,(linhas,colunas))
            bio = atualizaImagem(imgDeslocada)
            window["-imgEditada-"].update(data=bio.getvalue())
       
        if event == "Flip Horizontal": 
            img = cv2.imread(values["Arquivo"])   
            flipHoriz=cv2.flip(img,1)
            bio = atualizaImagem(flipHoriz)
            window["-imgEditada-"].update(data=bio.getvalue())
       
        if event == "Flip Vertical": 
            img = cv2.imread(values["Arquivo"])   
            flipVertical=cv2.flip(img,0)
            bio = atualizaImagem(flipVertical)
            window["-imgEditada-"].update(data=bio.getvalue())
       
        if event == "Flip Horizontal e Vertical": 
            img = cv2.imread(values["Arquivo"])   
            flipVertHori=cv2.flip(img,-1)
            bio = atualizaImagem(flipVertHori)
            window["-imgEditada-"].update(data=bio.getvalue())

        
        

        
            
            
    window.close()

if __name__ == "__main__":
    main()