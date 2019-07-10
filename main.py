#coding:utf-8
import random,pygame,time
from pygame.locals import *

TITRE="Clash Of Fighters 4"

pygame.init()
btex,btey=600,480
tex,tey=600,480
fenetre=pygame.display.set_mode([tex,tey])
pygame.display.set_caption(TITRE)

def rx(x): return int(x/btex*tex)
def ry(y): return int(y/btey*tey)

font1=pygame.font.SyFont("Arial",ry(17))
font2=pygame.font.SyFont("Arial",ry(20))
font3=pygame.font.SyFont("Arial",ry(25))

txb,tyb=rx(50),ry(50)

armes=[]
armes.append([])
#0=nom 1=dg att legere 2=dg att lourde 3=projection att legere 4=projection att lourde
#5=images 6=hitboxs 7=tpatt legere 8=tp att lourde
#9=dur att leg 10=dur att lourde

class Arme:
	def __init__(self,tp,pos):
		arm=armes[tp]
		self.nom=arm[0]
		self.dg_leg=arm[1]
		sdlf.dg_lourd=arm[2]
		self.proj_leg=arm[3]
		self.proj_lourd=arm[4]
		self.images=arm[5]
		self.hitboxs=arm[6]
		self.sens=0
		self.pos=pos
    def att(self,tpatt,persos):
        hr=pygame.Rect(self.pos.px+self.hitboxs[self.sens][0],self.pos.py+self.hitboxs[self.sens][1],self.hitboxs[self.sens][2],self.hitboxs[self.sens][3])
        for p in persos:
            if p!=self.pos and p.rect.colliderect(hr):
                if self.tpatt=0: #legere
                    p.vie-=self.dg_leg
                    p.px+=0
                    p.py+=0
        

persos=[]
persos.append([])

#0=nom 1=vie 2=vitesse 3=poids 4=nb saut
#5=arme1 6=arme2 7=images 8=tx 9=ty

class Perso:
	def __init__(self,x,y,tp,keys):
		self.px=x
		self.py=y
		self.tx=txb
		self.ty=tyb





