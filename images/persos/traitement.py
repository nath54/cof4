#coding:utf-8
import os
from PIL import Image

cl1=(0,0,0,255)
cl2=(255,0,0,255)

def trait_img(nf):
    img=Image.open(nf)
    im=img.load()
    tx,ty=img.size
    nimg=Image.new("RGBA",[tx,ty],(0,0,0,0))
    nim=nimg.load()
    print(tx,ty)
    for x in range(tx):
        for y in range(ty):
            #print(im[x,y],cl1)
            if im[x,y]==cl1:
                nim[x,y]=cl2
                #print("WARNING  : ",cl1,cl2)
            #else: nim[x,y]=im[x,y]
    nimg.save(nf, 'PNG')

dire="p4/"
for o in os.listdir(dire):
    if o[-4:]==".png":
        no="p4"+o[2:]
        print(o+" -> "+no)
        os.rename(dire+o,dire+no)
        try: trait_img(dire+no)
        except: print("error")
    

