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
    image.thumbnail((larguraTela/2, alturaTela/2)) 
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
            sg.Button("Espelhamento"),
            sg.Button("Translação"),
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
        
           #     sg.Button("Ajuste Escala"),
          #  sg.Button("Perspectiva"),
           # sg.Button("Rotacao"),
         #   sg.Button("Espelhamento"),
          #  sg.Button("Translação"),
        
        
            
            
    window.close()

if __name__ == "__main__":
    main()