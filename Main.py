import pygame, sys, os
from pygame.locals import QUIT

clear=lambda:os.system("clear")
pygame.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (50, 200, 50)
BLUE = (0, 0, 255)
GRAY=(50,50,50)
BROWN=(93,71,1)
YELLOW=(215,208,6)
FPS=24
size=50
screen = pygame.display.set_mode([600, 600])
clock = pygame.time.Clock()
whitePiecesCaptured=0
darkPiecesCaptured=0
font = pygame.font.Font('African-l6d.ttf', 27)
promote=False
#whitePiecesCaptured=14
from pygame.locals import (
  K_UP,
  K_DOWN,
  K_LEFT,
  K_RIGHT,
  K_ESCAPE,
  K_SPACE,
  KEYDOWN,
  QUIT,
  MOUSEMOTION,
  MOUSEBUTTONDOWN
)

class tile(pygame.sprite.Sprite):
  def __init__(self, x,y,color, col, row):
    pygame.sprite.Sprite.__init__(self)
    
    self.image=pygame.Surface((size,size))
    self.image.fill(color)
    self.originalcolor=color
    self.mask=pygame.mask.from_surface(self.image)
    #pygame.draw.rect(self.image, RED, pygame.Rect(x,y,size,size)) 
    self.rect=self.image.get_rect()
    self.rect.center=(x,y)
    self.col=col
    self.row=row
    letters="abcdefghi"
    mycol=letters[self.col-1]
    self.pos=mycol+str(self.row)
  def report(self):

    print(self.pos)
    

allsprites=pygame.sprite.Group()
pieces=pygame.sprite.Group()
tiles=pygame.sprite.Group()
rhinos=pygame.sprite.Group()
birds=pygame.sprite.Group()

pygame.event.pump()
#Piece classes: 
class bird(pygame.sprite.Sprite):
  def __init__(self,color, pos):
    global birds
    self.type="bird"
    pygame.sprite.Sprite.__init__(self)
    self.image=pygame.Surface((size,size))
    self.pos=pos
    self.color=color
    self.mask=pygame.mask.from_surface(self.image)
    if color=="light":    
      self.birdimage=pygame.image.load("LightBird.png").convert_alpha()
    else:
      self.birdimage=pygame.image.load("DarkBird.png").convert_alpha()
    self.birdimage=pygame.transform.scale(self.birdimage,(size,size))
    self.image=self.birdimage
    self.rect=self.image.get_rect()
    self.col=pos[0]
    self.col=8
    self.row=pos[1]
    self.row=int(self.row)
    self.rect.center = (self.col*size+75,size*(8-self.row)+75)
    pieces.add(self)
    allsprites.add(self)
    birds.add(self)
  def move(self,pos):
    if SearchTile(pos)=="":
      
      self.pos=pos
      self.col=pos[0]
      letters="abcdefghi"
      self.col=letters.index(self.col)
      self.row=pos[1]
      self.row=int(self.row)
      self.rect.center = (self.col*size+75,size*(8-self.row)+75)
      return True
    else:
      print("Illegal move")
      return False
  def attemptMove(self,dir):
    dest=TileScout(self.pos,dir)
    if dest=="":
      return False
    else:
      target=SearchTile(dest)
      if target=="":
        self.pos=dest
        self.col=dest[0]
        letters="abcdefghi"
        self.col=letters.index(self.col)
        self.row=dest[1]
        self.row=int(self.row)
        self.rect.center = (self.col*size+75,size*(8-self.row)+75)
        return True
      elif target.color!=self.color:
        return False
      else:
        ans=target.attemptMove(dir)
        if ans:
          self.pos=dest
          self.col=dest[0]
          letters="abcdefghi"
          self.col=letters.index(self.col)
          self.row=dest[1]
          self.row=int(self.row)
          self.rect.center = (self.col*size+75,size*(8-self.row)+75)
          return True
        else:
          return False
def shift(startpos,colchange,rowchange):
  col=startpos[0]
  letters="abcdefghi"
  col=letters.index(col)
  row=pos[1]
  row=int(row)
  newcol=col+colchange
  newcol=letters[newcol]
  newrow=row+rowchange
  newrow=str(newrow)
  return newcol+newrow
class rat(pygame.sprite.Sprite):
  def __init__(self,color, pos):
    
    self.type="rat"
    pygame.sprite.Sprite.__init__(self)
    self.image=pygame.Surface((size,size))
    self.pos=pos
    self.color=color
    self.mask=pygame.mask.from_surface(self.image)
    if color=="light":    
      self.ratimage=pygame.image.load("LightRat.png").convert_alpha()
    else:
      self.ratimage=pygame.image.load("DarkRat.png").convert_alpha()
    self.ratimage=pygame.transform.scale(self.ratimage,(size,size))
    self.image=self.ratimage
    self.rect=self.image.get_rect()
    self.col=pos[0]
    letters="abcdefghi"
    self.col=letters.index(self.col)
    self.row=pos[1]
    self.row=int(self.row)
    self.rect.center = (self.col*size+75,size*(8-self.row)+75)
    pieces.add(self)
    allsprites.add(self)
  def move(self,pos):
    global whitePiecesCaptured, darkPiecesCaptured
    global promote
    dest=SearchTile(pos)
    if dest=="" or dest.color != self.color:
      validmoves=[]
      if self.color=="light":
        validmoves.append(TileScout(self.pos,"northeast"))
        validmoves.append(TileScout(self.pos,"northwest"))
        validmoves.append(TileScout(self.pos,"north"))
      else:
        validmoves.append(TileScout(self.pos,"southeast"))
        validmoves.append(TileScout(self.pos,"southwest"))
        validmoves.append(TileScout(self.pos,"south"))
      if pos in validmoves:
        if TileScout(self.pos, "north") ==pos or TileScout(self.pos, "south")==pos:
          
          if dest!= "":
            
            capturePiece(dest)
            self.pos=pos
            self.col=pos[0]
            letters="abcdefghi"
            self.col=letters.index(self.col)
            self.row=pos[1]
            self.row=int(self.row)
            self.rect.center = (self.col*size+75,size*(8-self.row)+75)
            if self.color=="light" and self.row==8:
              promote=True
            if self.color=="dark" and self.row==1:
              promote=True
            return True
          else:
            print("Illegal Move")
            return False
        else:
          if dest=="":
            self.pos=pos
            self.col=pos[0]
            letters="abcdefghi"
            self.col=letters.index(self.col)
            self.row=pos[1]
            self.row=int(self.row)
            self.rect.center = (self.col*size+75,size*(8-self.row)+75)
            if self.color=="light" and self.row==8:
              promote=True
            if self.color=="dark" and self.row==1:
              promote=True
            return True
          else:
            print("llegal move")
            return False
      else:
        print("Illegal move 2")
        return False
    else:
      print("Illegal move")
      return False
  def attemptMove(self,dir):
    dest=TileScout(self.pos,dir)
    if dest=="":
      return False
    else:
      target=SearchTile(dest)
      if target=="":
        self.pos=dest
        self.col=dest[0]
        letters="abcdefghi"
        self.col=letters.index(self.col)
        self.row=dest[1]
        self.row=int(self.row)
        self.rect.center = (self.col*size+75,size*(8-self.row)+75)
        return True
      elif target.color!=self.color:
        return False
      else:
        ans=target.attemptMove(dir)
        if ans:
          self.pos=dest
          self.col=dest[0]
          letters="abcdefghi"
          self.col=letters.index(self.col)
          self.row=dest[1]
          self.row=int(self.row)
          self.rect.center = (self.col*size+75,size*(8-self.row)+75)
          return True
        else:
          return False
class snake(pygame.sprite.Sprite):
  def __init__(self,color, pos):
    self.type="snake"
    
    pygame.sprite.Sprite.__init__(self)
    self.image=pygame.Surface((size,size))
    self.pos=pos
    self.color=color.lower()
    self.mask=pygame.mask.from_surface(self.image)
    if color=="light":    
      self.ratimage=pygame.image.load("LightSnake.png").convert_alpha()
    else:
      self.ratimage=pygame.image.load("DarkSnake.png").convert_alpha()
    self.ratimage=pygame.transform.scale(self.ratimage,(size,size))
    self.image=self.ratimage
    self.rect=self.image.get_rect()
    self.col=pos[0]
    letters="abcdefghi"
    self.col=letters.index(self.col)
    self.row=pos[1]
    self.row=int(self.row)
    self.rect.center = (self.col*size+75,size*(8-self.row)+75)
    pieces.add(self)
    allsprites.add(self)
  def move(self,pos):
    global darkPiecesCaptured, whitePiecesCaptured
    
    validmoves=[]
    directions=["northeast","northwest","southeast","southwest"]
    for dir in directions:
      dest=TileScout(self.pos,dir)
      while True:

        if SearchTile(dest)=="":
          
          validmoves.append(dest)
        elif SearchTile(dest).color==self.color:
          validmoves.append(dest)
          break
        elif SearchTile(dest).color!=self.color:
          validmoves.append(dest)
          break
        dest=TileScout(dest, dir)
        if dest=="":
          break
    

    
    if self.color=="light":
      forward=TileScout(self.pos, "north")
      doubleforward=TileScout(forward, "north")
    if self.color=="dark":
      forward=TileScout(self.pos, "south")
      doubleforward=TileScout(forward, "south")
      
    validmoves.append(doubleforward)
    validmoves.append(forward)
    #print(validmoves)
    if pos in validmoves:
      if pos==doubleforward and SearchTile(forward)!="":
        capturePiece(SearchTile(forward))
      dest=SearchTile(pos)
      if dest != "":
        
        capturePiece(dest)
        
        
      self.pos=pos
      self.col=pos[0]
      letters="abcdefghi"
      self.col=letters.index(self.col)
      self.row=pos[1]
      self.row=int(self.row)
      self.rect.center = (self.col*size+75,size*(8-self.row)+75)
      return True
    else:
      print("Illegal move 2")
      return False
  def attemptMove(self,dir):
    dest=TileScout(self.pos,dir)
    if dest=="":
      return False
    else:
      target=SearchTile(dest)
      if target=="":
        self.pos=dest
        self.col=dest[0]
        letters="abcdefghi"
        self.col=letters.index(self.col)
        self.row=dest[1]
        self.row=int(self.row)
        self.rect.center = (self.col*size+75,size*(8-self.row)+75)
        return True
      elif target.color!=self.color:
        return False
      else:
        ans=target.attemptMove(dir)
        if ans:
          self.pos=dest
          self.col=dest[0]
          letters="abcdefghi"
          self.col=letters.index(self.col)
          self.row=dest[1]
          self.row=int(self.row)
          self.rect.center = (self.col*size+75,size*(8-self.row)+75)
          return True
        else:
          return False
      
class Rhino(pygame.sprite.Sprite):
  def __init__(self,color, pos):
    self.type="rhino"
    
    pygame.sprite.Sprite.__init__(self)
    self.image=pygame.Surface((size*1.6,size*.8))
    self.pos=(50,50)
    self.color=color.lower()
    self.mask=pygame.mask.from_surface(self.image)
    if color=="light":    
      self.ratimage=pygame.image.load("LightRhino.png").convert_alpha()
    else:
      self.ratimage=pygame.image.load("DarkRhino.png").convert_alpha()
    self.ratimage=pygame.transform.scale(self.ratimage,(size*1.6,size*.8))
    self.image=self.ratimage
    self.rect=self.image.get_rect()
    if self.color=="light":
      y=480
    else:
      y=30
    self.rect.center=(50+size*1.7*(pos-1),y)
    pieces.add(self)
    allsprites.add(self)
    rhinos.add(self)
  def move(self,pos):
    col=pos[0]
    if self.color=="dark":
      for row in range(8,0,-1):
        piece=SearchTile(col+str(row))
        if piece!="":
          if piece.type=="lion":
            break
          piece.kill()
          
    if self.color=="light":
      for row in range(0,9,1):
        piece=SearchTile(col+str(row))
        if piece!="":
          if piece.type=="lion":
            break
          piece.kill()
    self.kill()
    return True

    
class lion(pygame.sprite.Sprite):
  def __init__(self,color, pos):
    self.type="lion"
    
    pygame.sprite.Sprite.__init__(self)
    self.image=pygame.Surface((size,size))
    self.pos=pos
    self.color=color.lower()
    self.mask=pygame.mask.from_surface(self.image)
    if color=="light":    
      self.ratimage=pygame.image.load("LightLion.png").convert_alpha()
    else:
      self.ratimage=pygame.image.load("DarkLion.png").convert_alpha()
    self.ratimage=pygame.transform.scale(self.ratimage,(size,size))
    self.image=self.ratimage
    self.rect=self.image.get_rect()
    self.col=pos[0]
    letters="abcdefghi"
    self.col=letters.index(self.col)
    self.row=pos[1]
    self.row=int(self.row)
    self.rect.center = (self.col*size+75,size*(8-self.row)+75)
    pieces.add(self)
    allsprites.add(self)
  def move(self,pos):
    global whitePiecesCaptured, darkPiecesCaptured
    dest=SearchTile(pos)
    
    validmoves=[]

    validmoves.append(TileScout(self.pos,"north"))
    validmoves.append(TileScout(self.pos,"northeast"))
    validmoves.append(TileScout(self.pos,"east"))
    validmoves.append(TileScout(self.pos,"southeast"))
    validmoves.append(TileScout(self.pos,"south"))
    validmoves.append(TileScout(self.pos,"southwest"))
    validmoves.append(TileScout(self.pos,"west"))
    validmoves.append(TileScout(self.pos,"northwest"))
    
   
    
    
    
    
    print(validmoves)
    if pos in validmoves:
      num=validmoves.index(pos)
      dir=""
      directions=["north","northeast", "east","southeast","south","southwest","west","northwest"]
      dir=directions[num]
      target=SearchTile(pos)
      if target=="":
        self.pos=pos
        self.col=pos[0]
        letters="abcdefghi"
        self.col=letters.index(self.col)
        self.row=pos[1]
        self.row=int(self.row)
        self.rect.center = (self.col*size+75,size*(8-self.row)+75)
        return True
      elif target.color!=self.color:
        self.pos=pos
        self.col=pos[0]
        letters="abcdefghi"
        self.col=letters.index(self.col)
        self.row=pos[1]
        self.row=int(self.row)
        self.rect.center = (self.col*size+75,size*(8-self.row)+75)
        
        capturePiece(target)
        return True
      else:
        
        if SearchTile(pos).attemptMove(dir):
          self.pos=pos
          self.col=pos[0]
          letters="abcdefghi"
          self.col=letters.index(self.col)
          self.row=pos[1]
          self.row=int(self.row)
          self.rect.center = (self.col*size+75,size*(8-self.row)+75)
          return True
      #if dest!="" and dest.color==self.color: #Pushing
       # pushable=[]
        #if pos==TileScout(self.pos,"north"):
         # push=SearchTile(pos)
          #while TileScout(push, "north")!="":
            #new=TileScout(push, "north")
            #pushable.append(new)
            #push=new
      
    else:
      print("Illegal move 2")
      return False
class cheeta(pygame.sprite.Sprite):
  def __init__(self,color, pos):
    self.type="cheeta"
    pygame.sprite.Sprite.__init__(self)
    self.image=pygame.Surface((size,size))
    self.pos=pos
    self.color=color
    self.mask=pygame.mask.from_surface(self.image)
    if color=="light":    
      self.birdimage=pygame.image.load("LightCheeta.png").convert_alpha()
    else:
      self.birdimage=pygame.image.load("DarkCheeta.png").convert_alpha()
    self.birdimage=pygame.transform.scale(self.birdimage,(size,size))
    self.image=self.birdimage
    self.rect=self.image.get_rect()
    self.col=pos[0]
    letters="abcdefghi"
    self.col=letters.index(self.col)
    self.row=pos[1]
    self.row=int(self.row)
    self.rect.center = (self.col*size+75,size*(8-self.row)+75)
    pieces.add(self)
    allsprites.add(self)
  def attemptMove(self,dir):
    dest=TileScout(self.pos,dir)
    if dest=="":
      return False
    else:
      target=SearchTile(dest)
      if target=="":
        self.pos=dest
        self.col=dest[0]
        letters="abcdefghi"
        self.col=letters.index(self.col)
        self.row=dest[1]
        self.row=int(self.row)
        self.rect.center = (self.col*size+75,size*(8-self.row)+75)
        return True
      elif target.color!=self.color:
        return False
      else:
        ans=target.attemptMove(dir)
        if ans:
          self.pos=dest
          self.col=dest[0]
          letters="abcdefghi"
          self.col=letters.index(self.col)
          self.row=dest[1]
          self.row=int(self.row)
          self.rect.center = (self.col*size+75,size*(8-self.row)+75)
          return True
        else:
          return False
#

#Creating Pieces on Board
  def move(self, pos):
    directions=["north","northeast","east","southeast","south","southwest","west", "northwest"]
    validmoves=[]
    for dir in directions:
      
      dest=TileScout(self.pos, dir)
      while True:
        if SearchTile(dest)=="":
          
          validmoves.append(dest)
        elif SearchTile(dest).color==self.color:
          break
        elif SearchTile(dest).color!=self.color:
          validmoves.append(dest)
          break
        dest=TileScout(dest, dir)
        if dest=="":
          break
        #print(dest)
    if pos in validmoves:
      piece=SearchTile(pos)
      if piece!="":
        capturePiece(piece)
        piece.kill()
      self.pos=pos
      self.col=pos[0]
      letters="abcdefghi"
      self.col=letters.index(self.col)
      self.row=pos[1]
      self.row=int(self.row)
      self.rect.center = (self.col*size+75,size*(8-self.row)+75)
      return True
    else:
      return False







    
class Hippo(pygame.sprite.Sprite):
  def __init__(self,color, pos):
    self.type="Hippo"
    pygame.sprite.Sprite.__init__(self)
    self.image=pygame.Surface((size,size))
    self.pos=pos
    self.color=color
    self.mask=pygame.mask.from_surface(self.image)
    if color=="light":    
      self.birdimage=pygame.image.load("LightHippo.png").convert_alpha()
    else:
      self.birdimage=pygame.image.load("DarkHippo.png").convert_alpha()
    self.birdimage=pygame.transform.scale(self.birdimage,(size,size))
    self.image=self.birdimage
    self.rect=self.image.get_rect()
    self.col=pos[0]
    letters="abcdefghi"
    self.col=letters.index(self.col)
    self.row=pos[1]
    self.row=int(self.row)
    self.rect.center = (self.col*size+75,size*(8-self.row)+75)
    pieces.add(self)
    allsprites.add(self)
  def attemptMove(self,dir):
    dest=TileScout(self.pos,dir)
    if dest=="":
      return False
    else:
      target=SearchTile(dest)
      if target=="":
        self.pos=dest
        self.col=dest[0]
        letters="abcdefghi"
        self.col=letters.index(self.col)
        self.row=dest[1]
        self.row=int(self.row)
        self.rect.center = (self.col*size+75,size*(8-self.row)+75)
        return True
      elif target.color!=self.color:
        return False
      else:
        ans=target.attemptMove(dir)
        if ans:
          self.pos=dest
          self.col=dest[0]
          letters="abcdefghi"
          self.col=letters.index(self.col)
          self.row=dest[1]
          self.row=int(self.row)
          self.rect.center = (self.col*size+75,size*(8-self.row)+75)
          return True
        else:
          return False

  def move(self, pos):
    directions=["north","east","south","west"]
    validmoves=[]
    finalDir=""
    for dir in directions:
      #print(dir)
      dest=TileScout(self.pos, dir)
      while True:
        if pos==dest:
          finalDir=dir
        if SearchTile(dest)=="":
          
          validmoves.append(dest)
        elif SearchTile(dest).color==self.color:
          break
        elif SearchTile(dest).color!=self.color:
          validmoves.append(dest)
          break
        dest=TileScout(dest, dir)
        if dest=="":
          break
        #print(dest)
    if pos in validmoves:
      piece=SearchTile(pos)
      if piece!="":
      
        capturePiece(piece)
        piece.kill()
        self.pos=pos
        self.col=pos[0]
        letters="abcdefghi"
        self.col=letters.index(self.col)
        self.row=pos[1]
        self.row=int(self.row)

        self.rect.center = (self.col*size+75,size*(8-self.row)+75)
        target=TileScout(self.pos,finalDir)
        if piece.type!="rat":
          for i in range(2):
            
            if SearchTile(target) !="":
              capturePiece(SearchTile(target))
              #SearchTile(target).kill()
              
              self.pos=target
              self.col=target[0]
              letters="abcdefghi"
              self.col=letters.index(self.col)
              self.row=target[1]
              self.row=int(self.row)
  
              self.rect.center = (self.col*size+75,size*(8-self.row)+75)
              target=TileScout(self.pos,finalDir)
          return True
        else:
          return True
      else:
        self.pos=pos
        self.col=pos[0]
        letters="abcdefghi"
        self.col=letters.index(self.col)
        self.row=pos[1]
        self.row=int(self.row)
        self.rect.center = (self.col*size+75,size*(8-self.row)+75)
        return True
        
class Meerkat(pygame.sprite.Sprite):
  def __init__(self,color, pos):
    self.type="Meerkat"
    pygame.sprite.Sprite.__init__(self)
    self.image=pygame.Surface((size,size))
    self.pos=pos
    self.color=color
    self.mask=pygame.mask.from_surface(self.image)
    if color=="light":    
      self.birdimage=pygame.image.load("LightMeerkat.png").convert_alpha()
    else:
      self.birdimage=pygame.image.load("DarkMeerkat.png").convert_alpha()
    self.birdimage=pygame.transform.scale(self.birdimage,(size,size))
    self.image=self.birdimage
    self.rect=self.image.get_rect()
    self.col=pos[0]
    letters="abcdefghi"
    self.col=letters.index(self.col)
    self.row=pos[1]
    self.row=int(self.row)
    self.rect.center = (self.col*size+75,size*(8-self.row)+75)
    pieces.add(self)
    allsprites.add(self)
  def attemptMove(self,dir):
    dest=TileScout(self.pos,dir)
    if dest=="":
      return False
    else:
      target=SearchTile(dest)
      if target=="":
        self.pos=dest
        self.col=dest[0]
        letters="abcdefghi"
        self.col=letters.index(self.col)
        self.row=dest[1]
        self.row=int(self.row)
        self.rect.center = (self.col*size+75,size*(8-self.row)+75)
        return True
      elif target.color!=self.color:
        return False
      else:
        ans=target.attemptMove(dir)
        if ans:
          self.pos=dest
          self.col=dest[0]
          letters="abcdefghi"
          self.col=letters.index(self.col)
          self.row=dest[1]
          self.row=int(self.row)
          self.rect.center = (self.col*size+75,size*(8-self.row)+75)
          return True
        else:
          return False

    
  def move(self, pos):
    validmoves=[]
    directions=["north","northeast","east","southeast","south","southwest","west", "northwest"]
    
    n1=TileScout(self.pos,"north")
    n2=TileScout(n1,"north")
    ne=TileScout(n2,"east")
    nw=TileScout(n2,"west")
    
    s1=TileScout(self.pos,"south")
    s2=TileScout(s1,"south")
    se=TileScout(s2,"east")
    sw=TileScout(s2,"west")

    e1=TileScout(self.pos,"east")
    e2=TileScout(e1,"east")
    en=TileScout(e2,"north")
    es=TileScout(e2,"south")

    w1=TileScout(self.pos,"west")
    w2=TileScout(w1,"west")
    wn=TileScout(w2,"north")
    ws=TileScout(w2,"south")
    
    validmoves.append(nw)
    validmoves.append(ne)
    validmoves.append(sw)
    validmoves.append(se)
    validmoves.append(en)
    validmoves.append(es)
    validmoves.append(wn)
    validmoves.append(ws)
    
    if pos in validmoves:
      if SearchTile(pos)=="":
        self.pos=pos
        self.col=pos[0]
        letters="abcdefghi"
        self.col=letters.index(self.col)
        self.row=pos[1]
        self.row=int(self.row)
        self.rect.center = (self.col*size+75,size*(8-self.row)+75)
        print("col is", self.col)
        if self.col==0:
          bloc=SearchTile(letters[7]+str(self.row))
          if bloc =="":
            self.col=7 
            self.pos=letters[7]+str(self.row)
            self.rect.center = (self.col*size+75,size*(8-self.row)+75)
            print("burrowing")
            return True
          if bloc.color==self.color:
            print("could not burrow")
            return True
          if bloc.color!=self.color:
            capturePiece(bloc)
            self.col=7 
            self.pos=letters[7]+str(self.row)
            self.rect.center = (self.col*size+75,size*(8-self.row)+75)
            print("burrowing")
            return True
        elif self.col==7:
          bloc=SearchTile(letters[0]+str(self.row))
          if bloc =="":
            self.col=0 
            self.pos=letters[0]+str(self.row)
            self.rect.center = (self.col*size+75,size*(8-self.row)+75)
            print("burrowing")
            return True
          if bloc.color==self.color:
            print("could not burrow")
            return True
          if bloc.color!=self.color:
            capturePiece(bloc)
            self.col=0
            self.pos=letters[0]+str(self.row)
            self.rect.center = (self.col*size+75,size*(8-self.row)+75)
            print("burrowing")
            return True
        return True
        
      elif SearchTile(pos).color!=self.color:
        capturePiece(SearchTile(pos))
        self.pos=pos
        self.col=pos[0]
        letters="abcdefghi"
        self.col=letters.index(self.col)
        self.row=pos[1]
        self.row=int(self.row)
        self.rect.center = (self.col*size+75,size*(8-self.row)+75)
        return True
      elif SearchTile(pos).color==self.color:
        print("invalid move")
        return False
        
        
      
    
      
def setboard():
  global allsprites, pieces, promote, whitePiecesCaptured,darkPiecesCaptured,turn,arrow, sPiece, sTile, tiles
  sPiece=""
  sTile=""
  
  allsprites.empty()
  pieces.empty()
  tiles.empty()
  whitePiecesCaptured=0
  darkPiecesCaptured=0
  turn="light"
  promote=False
  arrow=pygame.transform.rotate(arrow, 180)
  tilecolor="BROWN"
  for x in range(1,9):
    for y in range(8,0,-1):
      if tilecolor=="BROWN":
        t=tile(x*50+25, y*50+25, BROWN, x,9-y)
        allsprites.add(t)
        tiles.add(t)
        tilecolor="YELLOW"
      else:
        t=tile(x*50+25, y*50+25, YELLOW,x,9-y)
        allsprites.add(t)
        tiles.add(t)
        tilecolor="BROWN"
    if tilecolor=="BROWN":
      tilecolor="YELLOW"
    else:
      tilecolor="BROWN"
  t=tile(475,425,BLUE,9,1)
  allsprites.add(t)
  tiles.add(t)
  t=tile(475,75,BLUE,9,8)
  allsprites.add(t)
  tiles.add(t)
  
  b=bird("light", "i1")
  b=bird("dark", "i8")
  
  s=snake("light", "c1")
  s=snake("light", "f1")
  s=snake("Dark", "c8")
  s=snake("Dark", "f8")
  
  for x in "abcdefgh":
    r=rat("light", x+"2")
  for x in "abcdefgh":
    r=rat("dark", x+"7")
    
  l=lion("light", "e1")
  l=lion("dark", "e8")
  
  c=cheeta("light", "d1")
  c=cheeta("dark","d8")
  
  h=Hippo("light","a1")
  h=Hippo("dark", "a8")
  h=Hippo("light", "h1")
  h=Hippo("dark", "h8")
  
  m=Meerkat("light", "g1")
  m=Meerkat("dark","b8")
  m=Meerkat("light", "b1")
  m=Meerkat("dark","g8")
#Utility
def SearchTile(pos):
  for p in pieces:
    if p.pos==pos:
      return p
  return ""
  
def TileScout(pos, dir):
  #Find whether a selection is on the board, and then the direction of the piece plus one
  if pos=="":
    return ""
  col=pos[0]
  letters=" abcdefghi"
  col=letters.index(col)
  row=pos[1]
  row=int(row)
  if dir=="north":
    if row==8:
      return ""
    else:
      return letters[(col)]+str(row+1)
  if dir=="northeast":
    if row==8 or col==8:
      return ""
    else:
      return letters[(col+1)]+str(row+1)
  if dir=="east":
    if col==8:
      return ""
    else:
      return letters[(col+1)]+str(row)
  if dir=="southeast":
    if row==1 or col==8:
      return ""
    else:
      return letters[(col+1)]+str(row-1)
  if dir=="south":
    if row==1:
      return ""
    else:
      return letters[(col)]+str(row-1)
  if dir=="southwest":
    if row==1 or col==1:
      return ""
    else:
      return letters[(col-1)]+str(row-1)
  if dir=="west":
    if col==1:
      return ""
    else:
      return letters[(col-1)]+str(row)
  if dir=="northwest":
    if row==8 or col==1:
      return ""
    else:
      return letters[(col-1)]+str(row+1)
gameover=False
def capturePiece(piece):
  global whitePiecesCaptured, darkPiecesCaptured, gameover
  if piece.color=="light":
    whitePiecesCaptured+=1
    #print(whitePiecesCaptured)
    if whitePiecesCaptured==5:
      r=Rhino("dark", 1)
    if whitePiecesCaptured==10:
      r=Rhino("dark", 2)
    if whitePiecesCaptured==15:
      r=Rhino("dark", 3)
  if piece.color=="dark":
    darkPiecesCaptured+=1
    #print(darkPiecesCaptured)
    if darkPiecesCaptured==5:
      r=Rhino("light", 1)
    if darkPiecesCaptured==10:
      r=Rhino("light", 2)
    if darkPiecesCaptured==15:
      r=Rhino("light", 3)
  if piece.type=="lion"and piece.color=="light":
    print("Dark Wins")
    gameover=True
  if piece.type=="lion"and piece.color=="dark":
    print("Light Wins")

    
    gameover=True
    
  piece.kill()

introSprites=pygame.sprite.Group()
helpSprites=pygame.sprite.Group()
NewGameGroup=pygame.sprite.Group()
PromoteGroup=pygame.sprite.Group()

class meerkatbutton(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.birdimage=pygame.image.load("MeerkatButton2.png").convert_alpha()                             
    self.image=self.birdimage
    self.rect=self.image.get_rect()
    self.rect.center=(175,25)
    self.image=pygame.transform.scale(self.image,(50,50))
    PromoteGroup.add(self)
    
meerkatbutton=meerkatbutton()

class cheetabutton(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.birdimage=pygame.image.load("CheetaButton2.png").convert_alpha()  
    self.image=self.birdimage
    self.rect=self.image.get_rect()
    self.rect.center=(125,25)
    self.image=pygame.transform.scale(self.image,(50,50))
    PromoteGroup.add(self)

cheetabutton=cheetabutton()
class startbutton(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.birdimage=pygame.image.load("StartButton.png").convert_alpha()
    self.image=self.birdimage
    self.rect=self.image.get_rect()
    self.rect.center=(450,350)
    self.image=pygame.transform.scale(self.image,(200,150))
    introSprites.add(self)
    
start=startbutton()

class helpbutton(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.birdimage=pygame.image.load("HelpButton.png").convert_alpha()
    self.image=self.birdimage
    self.rect=self.image.get_rect()
    self.rect.center=(463,500)
    self.image=pygame.transform.scale(self.image,(210,150))
    introSprites.add(self)
    
    
help=helpbutton()

class BackButton(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.birdimage=pygame.image.load("BackButton.png").convert_alpha()
    self.image=self.birdimage   
    self.image=pygame.transform.scale(self.image,(600,550))
    self.rect=self.image.get_rect()
    self.rect.center=(100,30)
    helpSprites.add(self)


class GameButton(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.birdimage=pygame.image.load("GameButton.png").convert_alpha()
    self.image=self.birdimage   
    self.image=pygame.transform.scale(self.image,(100,50))
    self.rect=self.image.get_rect()
    self.rect.center=(100,30)
    NewGameGroup.add(self)
GameButton=GameButton()
#Start Scree
font2 = pygame.font.Font('African-l6d.ttf', 40)
StartScreen=True
helpscreen=False
BackButton=BackButton()
while StartScreen:
  
  while StartScreen == True and helpscreen==False:
    
    background=pygame.image.load("Background.jpg")
    background=pygame.transform.scale(background,(600,600))
    screen.blit(background,(0,0))
    
    Welcome=pygame.image.load("SafariCHessTitle.png")
    Welcome=pygame.transform.scale(Welcome,(650,600))
    screen.blit(Welcome,(-25,0))
    
    
    
  
    introSprites.draw(screen)
  
    for event in pygame.event.get():
      if event.type==MOUSEBUTTONDOWN:
        x,y=event.pos
        if start.rect.collidepoint(x,y):
          StartScreen=False
        if help.rect.collidepoint(x,y):
          helpscreen=True
          StartScreen=False
      
    
    pygame.display.flip()
  
  #helpscreen
  while helpscreen:
    
    background=pygame.image.load("Background.jpg")
    background=pygame.transform.scale(background,(600,600))
    screen.blit(background,(0,0))
    
    helpscreen=pygame.image.load("HelpScreen.png")
    helpscreen=pygame.transform.scale(helpscreen,(600,500))
    screen.blit(helpscreen,(0,100))
  
    
    helpSprites.draw(screen)
    pygame.display.flip()
  
    for event in pygame.event.get():
      if event.type==MOUSEBUTTONDOWN:
        x,y=event.pos
        if BackButton.rect.collidepoint(x,y):
          helpscreen=False
          StartScreen=True
        
      

sPiece=""
screen = pygame.display.set_mode([500, 500])
#Main Loop
arrow=pygame.image.load("Arrow.png")
arrow=pygame.transform.scale(arrow,(50,50))
sTile=""
print("Welcome to safari chess \nlight moves first")
setboard()
while True:
  #promote=True

  
  clock.tick(FPS)
  for event in pygame.event.get():
    if event.type==MOUSEBUTTONDOWN:
      x,y=event.pos
      if gameover:
        if GameButton.rect.collidepoint(x,y):
          setboard()
          gameover=False
          arrow=pygame.image.load("Arrow.png")
          arrow=pygame.transform.scale(arrow,(50,50))
          arrow=pygame.transform.rotate(arrow, 180)
          break
      if promote:
        promotion=""
        if meerkatbutton.rect.collidepoint(x,y):
          promotion="meerkat"
          for p in pieces:
            if p.color=="light" and p.type=="rat" and p.row==8:
              Meerkat("light",p.pos)
              p.kill()
              promote=False
            if p.color=="dark" and p.type=="rat" and p.row==1:
              Meerkat("dark",p.pos)
              p.kill()
              promote=False
        if cheetabutton.rect.collidepoint(x,y):
          promotion="cheeta"
          for p in pieces:
            if p.color=="light" and p.type=="rat" and p.row==8:
              cheeta("light",p.pos)
              p.kill()
              promote=False
            if p.color=="dark" and p.type=="rat" and p.row==1:
              cheeta("dark",p.pos)
              p.kill()
              promote=False
          
          
          #break
      for s in tiles:
        if s.rect.collidepoint(x,y):
          #s.report()
          if sPiece=="":
            sTile=s
            sPiece=SearchTile(s.pos)
            print(sTile.pos+" selected")
            if sPiece=="":
              print("empty tile selected")
              sPiece="empty"
            else:
              print(sPiece.color+" "+sPiece.type+"selected")
              if sPiece.color!=turn:
                sPiece=""
                print("wrong color")
              else:
                s.image.fill(GREEN)
          else:
            if sPiece=="empty":
              sTile.image.fill(sTile.originalcolor)
              sPiece=""
            else:
              
              result=sPiece.move(s.pos)
              sPiece=""
              sTile.image.fill(sTile.originalcolor)
              if result:
                if turn=="light":
                  if gameover!=True:
                    turn="dark"
                    clear()
                    print("dark turn")
                    arrow=pygame.transform.rotate(arrow, 180)
                else:
                  if gameover!=True:
                    turn="light"
                    clear()
                    print("light Turn")
                    arrow=pygame.transform.rotate(arrow, 180)
              
      if sPiece=="":
        for r in rhinos:
          if r.rect.collidepoint(x,y):
            color=r.color
            print(color+"Rhino "+"selected")
            sPiece=r
        #for b in birds:
          #if b.rect.collidepoint(x,y):
            #sPiece=b
           # print(b.color+"Bird"+"selected")
            
            
      
  screen.fill(GRAY)
  allsprites.draw(screen)
  if promote==True:
    PromoteGroup.draw(screen)
  if gameover:
    NewGameGroup.draw(screen)
    
    
  whitepiecescapturedisplay = font.render("Captured: "+str(whitePiecesCaptured), True, WHITE, GRAY)
  
  blackpiecescapturedisplay = font.render("Captured: "+str(darkPiecesCaptured), True, WHITE, GRAY)

  screen.blit(whitepiecescapturedisplay,(270,10))
  screen.blit(blackpiecescapturedisplay,(270,460))
  screen.blit(arrow,(450,225))
  pygame.display.flip()

  
#Bird - Goes anywhere it wants But captures nothing
  
#Rats - Only can capture other rats - also can be promoted
  
#snakes - Can only eat rats and birds & possibly grow
  
#Rhinos - Clears a whole row even your own units
  
#Lion -  
  
#cheeta - Can move 5 spaces in any direction and can move and then attack, but only attacks diagonally, & can't attack lion
  
#elephants - can only move horizontally one space at a time, but when it captures another unit, it can attack again.
  
#Alligators - Two squares long can only move straight but can attack in all directions to all peices
  
#hippos can attack up to 2 spaces in froHippont and move
