#coding:utf-8
#!/bin/python3
import random,pygame,time,math
from pygame.locals import *

TITRE="Clash Of Fighters 4"

pygame.init()
btex,btey=1280,1024
io = pygame.display.Info()
tex,tey=io.current_w,io.current_h
fenetre=pygame.display.set_mode([tex,tey],pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF)
pygame.display.set_caption(TITRE)

import pygame
from pygame.locals import *

mon_joystick="joystick"
nb_joysticks = pygame.joystick.get_count()
if nb_joysticks > 0:
	mon_joystick = pygame.joystick.Joystick(0)
	mon_joystick.init()

strings=(
"        .       ",
"       ...      ",
"       ...      ",
"       ...      ",
"       ...      ",
"       ...      ",
"       ...      ",
"       ...      ",
"      .....     ",
"      .....     ",
"   XXXXXXXXXXX  ",
"  X...........X ",
"   XXXXXXXXXXX  ",
"       X.X      ",
"       X.X      ",
"        X       "
)


cursor,mask=pygame.cursors.compile(strings, black='X', white='.', xor='o')
cursor_sizer=((16,16),(9,8),cursor,mask)
pygame.mouse.set_cursor(*cursor_sizer)

def rx(x): return int(x/btex*tex)
def ry(y): return int(y/btey*tey)

dim="images/"
dimp="images/persos/"

fondmapes=[pygame.transform.scale(pygame.image.load(dim+"fondmape1.png"),[tex,tey]) ] #,pygame.transform.scale(pygame.image.load(dim+"fondmape2.png"),[tex,tey])]

font1=pygame.font.SysFont("Arial",ry(17))
font2=pygame.font.SysFont("Arial",ry(20))
font3=pygame.font.SysFont("Arial",ry(25))

txb,tyb=rx(75),ry(75)

mapes=[]
mapes.append( [ [rx(100),ry(500),rx(900),ry(300),(50,50,50)] ] )
mapes.append( [ [rx(100),ry(600),rx(300),ry(300),(90,90,90)] , [rx(700),ry(600),rx(300),ry(300),(90,90,90)] ] )


class Mape:
    def __init__(self,x,y,tx,ty,cl):
        self.px=x
        self.py=y
        self.tx=tx
        self.ty=ty
        self.cl=cl
        self.rect=pygame.Rect(self.px,self.py,self.tx,self.ty)
        self.recthaut=pygame.Rect(self.px+self.tx*0.01,self.py,self.tx*0.98,self.ty*0.01)
        self.rectgauche=pygame.Rect(self.px,self.py+self.ty*0.01,self.tx*0.01,self.ty*0.98)
        self.rectdroite=pygame.Rect(self.px+self.tx*0.99,self.py+self.ty*0.01,self.tx*0.01,self.ty*0.98)
        self.rectbas=pygame.Rect(self.px,self.py+self.ty*0.99,self.tx,self.ty*0.01)
        
xt=int(txb/2)
yt=int(tyb/2)

hitbox_poings=[[-xt,-tyb,txb,tyb],[-xt,tyb,txb,tyb],[0,-yt,txb,tyb],[-txb,-yt,txb,tyb]]
#0=haut 1=bas 2=droite 3=gauche
#xx+h[0] , yy+h[1] , h[2] , h[3]

armes=[]
armes.append(["poing",20,50,5,10,None,hitbox_poings,0.2,0.5,0.15,0.2])
#0=nom 1=dg att legere 2=dg att lourde 3=projection att legere 4=projection att lourde
#5=images 6=hitboxs 7=tpatt legere 8=tp att lourde
#9=dur att leg 10=dur att lourde

def dist(p1,p2): return int(math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2))

aproj=8

class Arme:
    def __init__(self,tp,pos):
        arm=armes[tp]
        self.nom=arm[0]
        self.dg_leg=arm[1]
        self.dg_lourd=arm[2]
        self.proj_leg=arm[3]
        self.proj_lourd=arm[4]
        self.images=arm[5]
        self.hitbox_att=arm[6]
        self.projs=[]
        self.sens=0
        self.pos=pos
        self.imgs=[[None],[None],[None],[None],[None],[None]]
        self.anims=self.imgs[0]
        self.an=0
        self.img=self.anims[self.an]
        self.datt_leg=time.time()
        self.datt_lourd=time.time()
        self.tatt_leg=arm[7]
        self.tatt_lourd=arm[8]
        self.dur_att_leg=arm[9]
        self.dur_att_lourd=arm[10]
    def att(self,tpatt,persos):
        xx=self.pos.px+self.pos.tx/2
        yy=self.pos.py+self.pos.ty/2
        for p in persos:
            if p!=self.pos:
                touche=False
                if self.pos.issenshaut:
                    hb=pygame.Rect(xx+self.hitbox_att[0][0],yy+self.hitbox_att[0][1],self.hitbox_att[0][2],self.hitbox_att[0][3])
                    if hb.colliderect(p.rect): touche=True
                if self.pos.issensbas and p.rect.colliderect(self.hitbox_att[1]):
                    hb=pygame.Rect(xx+self.hitbox_att[1][0],yy+self.hitbox_att[1][1],self.hitbox_att[1][2],self.hitbox_att[1][3])
                    if hb.colliderect(p.rect): touche=True
                if self.pos.issensdroite and p.rect.colliderect(self.hitbox_att[2]):
                    hb=pygame.Rect(xx+self.hitbox_att[2][0],yy+self.hitbox_att[2][1],self.hitbox_att[2][2],self.hitbox_att[2][3])
                    if hb.colliderect(p.rect): touche=True
                if self.pos.issensgauche and p.rect.colliderect(self.hitbox_att[3]):
                    hb=pygame.Rect(xx+self.hitbox_att[3][0],yy+self.hitbox_att[3][1],self.hitbox_att[3][2],self.hitbox_att[3][3])
                    if hb.colliderect(p.rect): touche=True
                if touche and not p.isesquive and not p.inv and tpatt==0: #att legere
                    p.vie-=self.dg_leg
                    if p.vie<=0: p.vie=1
                    p.vitx,p.vity=0,0
                    p.isenlair=True
                    if self.pos.issenshaut: p.vity-=self.proj_leg*((1.-(p.vie/p.vie_tot))*aproj)
                    if self.pos.issensbas: p.vity+=self.proj_leg*((1.-(p.vie/p.vie_tot))*aproj)
                    if self.pos.issensgauche: p.vitx-=self.proj_leg*((1.-(p.vie/p.vie_tot))*aproj)
                    if self.pos.issensdroite: p.vitx+=self.proj_leg*((1.-(p.vie/p.vie_tot))*aproj)
                    p.dtch=self.pos
                    p.dtpdtch=time.time()
                elif touche and not p.isesquive and not p.inv and tpatt==1: #att legere
                    p.vie-=self.dg_lourd
                    if p.vie<=0: p.vie=1
                    p.vitx,p.vity=0,0
                    p.isenlair=True
                    if self.pos.issenshaut: p.vity-=self.proj_lourd*((1.-(p.vie/p.vie_tot))*aproj)
                    if self.pos.issensbas: p.vity+=self.proj_lourd*((1.-(p.vie/p.vie_tot))*aproj)
                    if self.pos.issensgauche: p.vitx-=self.proj_lourd*((1.-(p.vie/p.vie_tot))*aproj)
                    if self.pos.issensdroite: p.vitx+=self.proj_lourd*((1.-(p.vie/p.vie_tot))*aproj)
                    p.dtch=self.pos
                    p.dtpdtch=time.time()
                    
                    
        

persos=[]
persos.append(["stickman","p1",1000,2,5,0.8,50,3,2,0,0])
persos.append(["stickman2","p2",1000,2,5,0.8,50,3,2,0,0])
persos.append(["stickman3","p3",1000,2,5,0.8,50,3,2,0,0])

#0=nom 1=nom image 2=vie 3=acceleration 4=vitese max 5=decceleration 6=poids 7=nbsauts 8=temps entre chaque esquive 9=arme1 10=arme2

def load_imgs(nim):
    imgs=[]
    for x in range(17): imgs.append([])
    for x in range(1,4): imgs[0].append( pygame.transform.scale(pygame.image.load(dimp+nim+"/"+nim+"-idle-"+str(x)+".png") , [txb,tyb] ) )
    for x in range(1,4): imgs[1].append( pygame.transform.scale(pygame.image.load(dimp+nim+"/"+nim+"-move_right-"+str(x)+".png") , [txb,tyb] ) )
    for x in range(1,4): imgs[2].append( pygame.transform.scale(pygame.image.load(dimp+nim+"/"+nim+"-move_left-"+str(x)+".png") , [txb,tyb] ) )
    for x in range(1,4): imgs[3].append( pygame.transform.scale(pygame.image.load(dimp+nim+"/"+nim+"-jump-"+str(x)+".png") , [txb,tyb] ) )
    for x in range(1,4): imgs[4].append( pygame.transform.scale(pygame.image.load(dimp+nim+"/"+nim+"-crouch-"+str(x)+".png") , [txb,tyb] ) )
    for x in range(1,4): imgs[5].append( pygame.transform.scale(pygame.image.load(dimp+nim+"/"+nim+"-att_leg-right-"+str(x)+".png") , [txb,tyb] ) )
    for x in range(1,4): imgs[6].append( pygame.transform.scale(pygame.image.load(dimp+nim+"/"+nim+"-att_leg-left-"+str(x)+".png") , [txb,tyb] ) )
    for x in range(1,4): imgs[7].append( pygame.transform.scale(pygame.image.load(dimp+nim+"/"+nim+"-att_leg-down-right-"+str(x)+".png") , [txb,tyb] ) )
    for x in range(1,4): imgs[8].append( pygame.transform.scale(pygame.image.load(dimp+nim+"/"+nim+"-att_leg-down-left-"+str(x)+".png") , [txb,tyb] ) )
    for x in range(1,4): imgs[9].append( pygame.transform.scale(pygame.image.load(dimp+nim+"/"+nim+"-att_leg-up-right-"+str(x)+".png") , [txb,tyb] ) )
    for x in range(1,4): imgs[10].append( pygame.transform.scale(pygame.image.load(dimp+nim+"/"+nim+"-att_leg-up-left-"+str(x)+".png") , [txb,tyb] ) )
    for x in range(1,4): imgs[11].append( pygame.transform.scale(pygame.image.load(dimp+nim+"/"+nim+"-att_leg-down-"+str(x)+".png") , [txb,tyb] ) )
    for x in range(1,4): imgs[12].append( pygame.transform.scale(pygame.image.load(dimp+nim+"/"+nim+"-att_leg-up-"+str(x)+".png") , [txb,tyb] ) )
    imgs[13].append( pygame.transform.scale(pygame.image.load(dimp+nim+"/"+nim+"-dodge.png") , [txb,tyb] ) )
    imgs[14].append( pygame.transform.scale(pygame.image.load(dimp+nim+"/"+nim+"-icon.png") , [txb,tyb] ) )
    imgs[15].append( pygame.transform.scale(pygame.image.load(dimp+nim+"/"+nim+"-side_mur-left.png") , [txb,tyb] ) )
    imgs[16].append( pygame.transform.scale(pygame.image.load(dimp+nim+"/"+nim+"-side_mur-right.png") , [txb,tyb] ) )
    #0=idle 1=move droite 2=move gauche 3=sauter 4=accroupis 5=att leg droite 6=att leg gauche 7=att leg bas droite 8=att leg bas gauche
    #9=att leg haut droite 10=att leg haut gauche 11=att leg bas 12=att leg haut 13=esquive 14=icon 15=mur cote gauche 16=mur cote droit
    return imgs

class Perso:
    def __init__(self,x,y,tp,keys,isbot):
        pp=persos[tp]
        self.isbot=isbot
        self.px=x
        self.py=y
        self.tx=txb
        self.ty=tyb
        self.vitx=0
        self.vity=0
        self.dbg=time.time()
        self.tbg=0.01
        self.nom=pp[0]
        self.nim=pp[1]
        self.vie_tot=pp[2]
        self.vie=self.vie_tot
        self.acc=pp[3]
        self.vit_max=pp[4]
        self.decc=pp[5]
        self.poids=pp[6]
        self.nbsaut_tot=pp[7]
        self.tesq=pp[8]
        self.nbsaut=self.nbsaut_tot
        self.imgs=load_imgs(self.nim)
        self.anim=self.imgs[0]
        self.an=0
        self.img=self.anim[self.an]
        self.dan=time.time()
        self.tan=0.1
        self.issenshaut=True
        self.issensbas=False
        self.issensdroite=False
        self.issensgauche=False
        self.inv=True
        self.dinv=time.time()
        self.tinv=3
        self.app=True
        self.dapp=time.time()
        self.tapp=0.1
        self.rect=pygame.Rect(self.px,self.py,self.tx,self.ty)
        self.isacroupi=False
        self.isesquive=False
        self.isenlair=True
        self.desq=time.time()
        self.duresq=0.7
        self.keys=keys
        self.djmp=time.time()
        self.tjmp=0.2
        self.mort=False
        self.arme_base=Arme(0,self)
        self.arme1=Arme(pp[10],self)
        self.arme2=Arme(pp[9],self)
        self.arme_actu=self.arme_base
        self.isimobilise=False
        self.points=0
        self.dtch=None
        self.dtpdtch=time.time()
        self.cible=None
        self.dcibl=time.time()
        self.tcibl=10
        self.dmv="left"
    def bouger(self,aa):
        if not self.mort:
            if aa=="left":
                self.dmv="left"
                self.issensgauche=True
                self.vitx-=self.acc
                if self.vitx<-self.vit_max: self.vitx=-self.vit_max
                if self.anim!=self.imgs[2] and not self.anim in [self.imgs[15]]:
                    self.anim=self.imgs[2]
                    self.an=0
                    self.img=self.anim[self.an]
                    self.dan=time.time()
                self.isenlair=True
                if self.isacroupi: self.isacroupi=False
            if aa=="right":
                self.dmv="right"
                self.issensdroite=True
                self.vitx+=self.acc
                if self.vitx>self.vit_max: self.vitx=self.vit_max
                if self.anim!=self.imgs[1] and not self.anim in [self.imgs[16]]:
                    self.anim=self.imgs[1]
                    self.an=0
                    self.img=self.anim[self.an]
                    self.dan=time.time()
                self.isenlair=True
                if self.isacroupi: self.isacroupi=False
            elif aa=="down":
                self.dmv="down"
                self.issensbas=True
                self.vity+=self.acc
                if self.vity>self.vit_max*3: self.vity=self.vit_max
                if self.anim!=self.imgs[4]:
                    self.anim=self.imgs[4]
                    self.an=0
                    self.img=self.anim[self.an]
                    self.dan=time.time()
                self.isenlair=True
                self.isacroupi=True
    def sauter(self):
        if not self.mort:
            if self.nbsaut > 0 and time.time()-self.djmp>=self.tjmp:
                self.djmp=time.time()
                self.vity-=5*self.vit_max
                self.nbsaut-=1
                if self.anim!=self.imgs[3]:
                    self.anim=self.imgs[3]
                    self.an=0
                    self.img=self.anim[self.an]
                    self.dan=time.time()
                self.isenlair=True
                if self.isacroupi: self.isacroupi=False
    def esquive(self):
        if not self.mort:
            if time.time()-self.desq>=self.tesq:
                self.desq=time.time()
                self.isesquive=True
                if self.issensgauche or self.issensdroite: self.vitx*=5
                if self.anim!=self.imgs[13]:
                    self.anim=self.imgs[13]
                    self.an=0
                    self.img=self.anim[self.an]
                    self.dan=time.time()
                if self.isenlair and self.nbsaut < self.nbsaut_tot:
                    self.nbsaut+=1
    def attaque_legere(self,persos):
        if not self.mort and time.time()-self.arme_actu.datt_leg>=self.arme_actu.tatt_leg:
            self.arme_actu.datt_leg=time.time()
            if self.issenshaut:
                if self.issensgauche:
                    self.anim=self.imgs[10]
                elif self.issensdroite:
                    self.anim=self.imgs[9]
                else:
                    self.anim=self.imgs[12]
            elif self.issensbas:
                if self.issensgauche:
                    self.anim=self.imgs[8]
                elif self.issensdroite:
                    self.anim=self.imgs[7]
                else:
                    self.anim=self.imgs[11]
            elif self.issensgauche:
                self.anim=self.imgs[6]
            elif self.issensdroite:
                self.anim=self.imgs[5]
            self.an=0
            self.img=self.anim[self.an]
            self.dan=time.time()
            self.arme_actu.att(0,persos)
    def attaque_lourde(self,persos):
        if not self.mort and time.time()-self.arme_actu.datt_lourd>=self.arme_actu.tatt_lourd:
            self.arme_actu.datt_lourd=time.time()
            if self.issenshaut:
                if self.issensgauche:
                    self.anim=self.imgs[10]
                elif self.issensdroite:
                    self.anim=self.imgs[9]
                else:
                    self.anim=self.imgs[12]
            elif self.issensbas:
                if self.issensgauche:
                    self.anim=self.imgs[8]
                elif self.issensdroite:
                    self.anim=self.imgs[7]
                else:
                    self.anim=self.imgs[11]
            elif self.issensgauche:
                self.anim=self.imgs[6]
            elif self.issensdroite:
                self.anim=self.imgs[5]
            self.an=0
            self.img=self.anim[self.an]
            self.dan=time.time()
            self.arme_actu.att(1,persos)
    def update(self,mape,persos):
        if self.isbot and time.time()-self.dcibl>=self.tcibl:
            self.dcible=time.time()
            self.cible=random.choice(persos)
            while self.cible==self: self.cible=random.choice(persos)
        if not self.mort:
            if time.time()-self.dan>=self.tan:
                self.dan=time.time()
                if self.an<len(self.anim)-1: self.an+=1
                if self.an>=len(self.anim)-1 and not self.isacroupi and not self.isenlair and not self.isesquive:
                    self.an=0
                    if self.anim not in [self.imgs[15],self.imgs[16]]: self.anim=self.imgs[0]
                if self.an < len(self.anim):
                    self.img=self.anim[self.an]
            if time.time()-self.desq>=self.duresq:
                self.isesquive=False
            if self.inv and time.time()-self.dinv>=self.tinv: self.inv=False
            elif self.inv:
                if time.time()-self.dapp>=self.tapp:
                    self.dapp=time.time()
                    self.app=not self.app
            if time.time()-self.dbg >= self.tbg and not self.isimobilise:
                self.dbg=time.time()
                if self.isenlair and not self.isesquive and self.vity < self.vit_max*0.8: self.vity+=2.5
                self.px+=self.vitx
                self.py+=self.vity
                if self.py>=tey:
                    self.mort=True
                    self.vie=0
                if self.px<=-tex or self.px>=tex*2: self.mort=True
                if self.py<=-1.0*tey: self.mort=True
                self.rect=pygame.Rect(self.px,self.py,self.tx,self.ty)
                for m in mape:
                    if self.rect.colliderect(m.rect):
                        h=True
                        if not self.rect.colliderect(m.rectbas):
                            if self.rect.colliderect(m.recthaut):
                                self.py-=self.vity
                                h=False
                            if self.rect.colliderect(m.rectgauche):
                                self.px-=self.vitx
                                if h: self.anim,self.an=self.imgs[15],0
                            if self.rect.colliderect(m.rectdroite):
                                self.px-=self.vitx
                                if h: self.anim,self.an=self.imgs[16],0
                            self.nbsaut=self.nbsaut_tot
                            self.isenlair=False   
                        if self.rect.colliderect(m.rectbas):
                            self.px-=self.vitx
                            self.py-=self.vity
                if self.vitx >= self.decc: self.vitx-=self.decc
                if self.vitx <= -self.decc: self.vitx+=self.decc
                if self.vity >= self.decc: self.vity-=self.decc
                if self.vity <= -self.decc: self.vity+=self.decc
                if self.vitx > 0 and self.vitx < self.decc: self.vitx=0
                if self.vitx < 0 and self.vitx > -self.decc: self.vitx=0
                if self.vity > 0 and self.vity < self.decc: self.vity=0
                if self.vity < 0 and self.vity > -self.decc: self.vity=0









def verif_keys(persos):
    key=pygame.key.get_pressed()
    for p in persos:
        if not p.isbot:
            if type(p.keys)==list:
                p.issenshaut=False
                p.issensbas=False
                p.issensgauche=False
                p.issensdroite=False
                isatt=False
                isesq=False
                if key[p.keys[0]]: #up
                    p.issenshaut=True
                if key[p.keys[1]]: #down
                    p.issensbas=True
                if key[p.keys[2]]: #left
                    p.issensgauche=True
                if key[p.keys[3]]: #right
                    p.issensdroite=True
                if key[p.keys[4]]: #sauter
                    p.sauter()
                if not p.issenshaut and not p.issensbas and not p.issensgauche and not p.issensdroite: p.issensdroite=True
                if key[p.keys[5]]: #attaque legere
                    p.attaque_legere(persos)
                    isatt=True
                if key[p.keys[6]]: #attaque lourde
                    p.attaque_lourde(persos)
                    isatt=True
                if key[p.keys[7]]: #esquive
                    p.esquive()
                    isesq=True
                if not isesq and not isatt:
                    if key[p.keys[0]]: #up
                        p.bouger("up")
                    if key[p.keys[1]]: #down
                        p.bouger("down")
                    if key[p.keys[2]]: #left
                        p.bouger("left")
                    if key[p.keys[3]]: #right
                        p.bouger("right")
            elif p.keys==mon_joystick:
                if mon_joystick.get_numaxes() >=4 and mon_joystick.get_numbuttons() >=10:
                    p.issenshaut=False
                    p.issensbas=False
                    p.issensgauche=False
                    p.issensdroite=False
                    isatt=False
                    isesq=False
                    #haut-bas
                    aa=float(mon_joystick.get_axis(1))
                    if aa > 0: aa=1
                    elif aa < -0.5 : aa=-1
                    else: aa=0 
                    if aa==-1: p.issenshaut=True
                    if aa==1: p.issensbas=True
                    #haut-bas
                    aa=float(mon_joystick.get_axis(0))
                    if aa > 0: aa=1
                    elif aa < -0.5 : aa=-1
                    else: aa=0 
                    if aa==-1: p.issensgauche=True
                    if aa==1: p.issensdroite=True
                    if not p.issenshaut and not p.issensbas and not p.issensgauche and not p.issensdroite: p.issensdroite=True
                    #sauter
                    if mon_joystick.get_button(0)==1:
                        p.sauter()
                    if mon_joystick.get_button(4)==1 or mon_joystick.get_button(5)==1:
                        p.esquive()
                        isesq=True
                    if mon_joystick.get_button(2)==1:
                        p.attaque_legere(persos)
                        isatt=True
                    if mon_joystick.get_button(1)==1:
                        p.attaque_lourde(persos)
                        isatt=True
                    if not isatt and not isesq:
                        #haut-bas
                        aa=float(mon_joystick.get_axis(1))
                        if aa > 0: aa=1
                        elif aa < -0.5 : aa=-1
                        else: aa=0 
                        if aa==-1: p.bouger("up")
                        if aa==1: p.bouger("down")
                        #haut-bas
                        aa=float(mon_joystick.get_axis(0))
                        if aa > 0: aa=1
                        elif aa < -0.5 : aa=-1
                        else: aa=0 
                        if aa==-1: p.bouger("left")
                        if aa==1: p.bouger("right")
                    if not p.issenshaut and not p.issensbas and not p.issensgauche and not p.issensdroite: p.issensdroite=True
    return persos
        
        
diff=1
def bot(persos):
    for p in persos:
        if p.isbot and not p.mort and random.randint(1,diff)==1:
            p.issenshaut=False
            p.issensbas=False
            p.issensgauche=False
            p.issensdroite=False
            bgv=0
            bgh=0
            att=0
            esquive=0
            if p.cible!=None:
                pp=p.cible
                if p.px+p.tx/2>pp.px+pp.tx/2 and abs((p.px+p.tx/2)-(pp.px+pp.tx/2)) > 60: bgh=-1
                if p.px+p.tx/2<pp.px+pp.tx/2 and abs((p.px+p.tx/2)-(pp.px+pp.tx/2)) > 60: bgh=1
                if p.py+p.ty/2>pp.py+pp.ty/2 and abs((p.py+p.ty/2)-(pp.py+pp.ty/2)) > 60: bgv=-1
                if p.py+p.ty/2<pp.py+pp.ty/2 and abs((p.py+p.ty/2)-(pp.py+pp.ty/2)) > 60: bgv=1
                if (time.time()-pp.arme_actu.datt_leg<=0.5) or (time.time()-pp.arme_actu.datt_lourd<=0.5): esquive=1
                if time.time()-p.arme_actu.datt_leg>=p.arme_actu.tatt_leg and dist([p.px,p.py],[pp.px,pp.py]) <= 100: att=1
                if time.time()-p.arme_actu.datt_lourd>=p.arme_actu.tatt_lourd and dist([p.px,p.py],[pp.px,pp.py]) <= 100: att=2
                if att==0:
                    if bgv==-1: p.sauter()
                    if bgv==1: p.bouger("down")
                    if bgh==-1: p.bouger("left")
                    if bgh==1: p.bouger("right")
                    if not p.issenshaut and not p.issensbas and not p.issensgauche and not p.issensdroite: p.issenshaut=True
                    if esquive==1: p.esquive()
                else:
                    if bgv==-1: p.issenshaut=True
                    if bgv==1: p.issensbas=True
                    if bgh==-1: p.issensgauche=True
                    if bgh==1: p.issensdroite=True
                    if not p.issenshaut and not p.issensbas and not p.issensgauche and not p.issensdroite: p.issenshaut=True
                    if att==1:
                        p.attaque_legere(persos)
                    elif att==2:
                        p.attaque_lourde(persos)
            else:
                aaa=random.choice(["up","down","left","right"])
                if aaa=="up": p.issenshaut=True
                elif aaa=="down": p.issensbas=True
                elif aaa=="left": p.issensgauche=True
                elif aaa=="right": p.issensdroite=True
                if random.randint(1,10)==1: #attaque ou pas
                    if random.randint(0,1)==0: p.attaque_legere(persos)
                    else: p.attaque_lourde(persos)
                else:
                    aaa=["up","down","left","right"]
                    for x in range(5): aaa.append(p.dmv)
                    bbb=random.choice(aaa)
                    if bbb!="up":
                        p.bouger(bbb)
                    else: p.sauter()
                
            
            
            
    

def aff_jeu(pause,persos,mape,cam,fondmape,fps):
    bts=[]
    for x in range(6): bts.append(None)
    fenetre.blit(fondmape,[0,0])
    #fenetre.fill((200,200,150))
    if not pause:
        for m in mape:
            pygame.draw.rect( fenetre , m.cl , ( cam[0]+m.px , cam[1]+m.py , m.tx , m.ty ) , 0)
            pygame.draw.rect( fenetre , (1,1,1) , (cam[0]+m.px+m.tx*0.01,cam[1]+m.py,m.tx*0.98,m.ty*0.01) , 2)
            pygame.draw.rect( fenetre , (1,1,1) , (cam[0]+m.px,cam[1]+m.py+m.ty*0.01,m.tx*0.01,m.ty*0.98) , 2)
            pygame.draw.rect( fenetre , (1,1,1) , (cam[0]+m.px+m.tx*0.99,cam[1]+m.py+m.ty*0.01,m.tx*0.01,m.ty*0.98) , 2)
            pygame.draw.rect( fenetre , (1,1,1) , (cam[0]+m.px,cam[1]+m.py+m.ty*0.99,m.tx,m.ty*0.01) , 2)
        xx,yy=rx(100),ry(25)
        for p in persos:
            if ( p.inv and not p.app ): pass
            elif p.mort:
                pass
            else:
                fenetre.blit( p.img , [cam[0]+p.px,cam[1]+p.py] )
            fenetre.blit( p.imgs[14][0] , [xx,yy] )
            pygame.draw.rect( fenetre , (0,0,0) , (xx,yy,txb,tyb) , 2 )
            if p.vie>=0:
                pygame.draw.rect( fenetre , (int(p.vie/p.vie_tot*255.),0,0) , (xx,yy+tyb+ry(5),int(p.vie/p.vie_tot*txb),ry(7)) , 0 )
            pygame.draw.rect( fenetre , (0,0,0) , (xx,yy+tyb+ry(5),txb,ry(7)) , 2 )
            pygame.draw.rect( fenetre , (255,255,255) , (xx+txb+rx(5),yy+tyb-ry(5),rx(20),ry(20)) , 0 )
            pygame.draw.rect( fenetre , (0,0,0) , (xx+txb+rx(5),yy+tyb-ry(5),rx(20),ry(20)) , 1 )
            fenetre.blit( font1.render(str(p.points),20,(0,0,0)) , [xx+txb+rx(7),yy+tyb-ry(3)] )
            xx+=rx(150)
    else:
        pygame.draw.rect(fenetre,(25,105,150),( rx(50),ry(50),rx(500),ry(924) ),0)
        pygame.draw.rect(fenetre,(0,0,0),( rx(50),ry(50),rx(500),ry(924) ),3)
        bts[0]=pygame.draw.rect(fenetre,(25,50,150),( rx(100),ry(150),rx(300),ry(75) ),0)
        fenetre.blit( font3.render("reprendre",25,(255,255,255)) , [rx(125),ry(175)] )
        bts[1]=pygame.draw.rect(fenetre,(25,50,150),( rx(100),ry(250),rx(300),ry(75) ),0)
        fenetre.blit( font3.render("ne fait rien",25,(255,255,255)) , [rx(125),ry(275)] )
        bts[2]=pygame.draw.rect(fenetre,(25,50,150),( rx(100),ry(350),rx(300),ry(75) ),0)
        fenetre.blit( font3.render("ne fait rien",25,(255,255,255)) , [rx(125),ry(375)] )
        bts[3]=pygame.draw.rect(fenetre,(25,50,150),( rx(100),ry(450),rx(300),ry(75) ),0)
        fenetre.blit( font3.render("quitter",25,(255,255,255)) , [rx(125),ry(475)] )
    fenetre.blit(font1.render("fps : "+str(fps),20,(255,255,255)),[rx(15),ry(15)])
    pygame.display.update()
    return bts


def main_jeu(nbpersos):
    spawnpoints=[[rx(100),ry(50)],[rx(200),ry(50)],[rx(300),ry(50)],[rx(400),ry(50)],[rx(500),ry(50)],[rx(600),ry(50)]]
    persos=[]
    k=[]
    if nb_joysticks > 0: k.append( mon_joystick )
    k.append([K_UP,K_DOWN,K_LEFT,K_RIGHT,K_KP0,K_KP1,K_KP2,K_KP3,K_KP4])
    k.append(None)
    bt=[False,False,True]
    for x in range(nbpersos):
        sp=random.choice(spawnpoints)
        if sp in spawnpoints: del(spawnpoints[spawnpoints.index(sp)])
        persos.append( Perso(sp[0],sp[1],x,k[x],bt[x]) )
    spawnpoints=[[rx(100),ry(50)],[rx(200),ry(50)],[rx(300),ry(50)],[rx(400),ry(50)],[rx(500),ry(50)],[rx(600),ry(50)]]
    pause=False
    encour=True
    cam=[0,0]
    mape=[]
    mp=random.choice(mapes)
    for m in mp:
        mape.append( Mape(m[0],m[1],m[2],m[3],m[4]) )
    fondmape=random.choice(fondmapes)
    bts=[]
    fps=0
    while encour:
        t1=time.time()
        bts=aff_jeu(pause,persos,mape,cam,fondmape,fps)
        verif_keys(persos)
        bot(persos)
        for p in persos:
            p.update(mape,persos)
        for p in persos:
            if p.mort:
                if p.dtch!=None and time.time()-p.dtpdtch<=10:
                    p.dtch.points+=2
                else: p.points-=2
                p.points-=1
                sp=random.choice(spawnpoints)
                p.vie=p.vie_tot
                p.isenlair=True
                p.inv=True
                p.dinv=time.time()
                p.px=sp[0]
                p.py=sp[1]
                p.dtch=None
                p.mort=False
                
        for event in pygame.event.get():
            if event.type==QUIT: exit()
            elif event.type==KEYDOWN:
                if event.key==K_ESCAPE:
                    pause=not pause
            elif event.type==JOYBUTTONDOWN:
                if mon_joystick.get_button(7)==1: pause=not pause
            elif event.type==MOUSEBUTTONUP:
                pos=pygame.mouse.get_pos()
                for b in bts:
                    if b!=None and b.collidepoint(pos):
                        di=bts.index(b)
                        if di==0: pause=False
                        elif di==3: encour=False
        t2=time.time()
        tt=(t2-t1)
        if tt!=0: fps=int(1./tt)













def aff_menu(menu):
    bts=[]
    for x in range(6): bts.append(None)
    fenetre.fill((0,0,0))
    pygame.display.update()
    return bts




def main():
    bts=[]
    menu=0
    encoure=True
    while encoure:
        pos=pygame.mouse.get_pos()
        bts=aff_menu(menu)
        for event in pygame.event.get:
            if event.type==QUIT: exit()
            elif event.type==KEYDOWN:
                if event.key==K_ESCAPE: encoure=False
            elif event.type==MOUSEBUTTONUP:
                pass

main_jeu(3)

