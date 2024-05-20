from Tetris import tetris
from copy import deepcopy
from random import choice, randrange, randint, Random
import pygame

W, H = 10, 20
TILE = 45
GAME_RES = W * TILE, H * TILE
RES = 750, 940
FPS = 60

class tplayer():
    def __init__(self, tetris):
        self.movementCount = 10
        self.step = 2
        self.tetriserasedlines = 0
        self.tempScore = 0
        self.status = "thinking"
        self.playabletetris = deepcopy(tetris)
        self.MovementOporunity = 10
        self.MovementPosibilities = 10
        self.lineErased = 0
        self.maxRow = 20
        self.maxScoreChoice = [0, 0, 0, 1]      #0 = r,  1= x ,  2 = score, 3: (1 = left, -1 right)

    def setMaxScoreChoice(self, r, x, score, direction, tetris):

        #Cuenta que tan alto esta la linea
        self.maxRow = tetris.calculateNumberOfRows()
        #Weightedscore = 1000000 + -(20-self.maxRow)*(20-self.maxRow)*500 +self.yfactor*10000 + tetris.erasedLinedCount*20000 - tetris.trash()*100000 - tetris.gameover*1000000
        #Weightedscore = 1000000 + -(20-self.maxRow)*(20-self.maxRow)*500 +self.yfactor*10000 + tetris.erasedLinedCount*1000000 - tetris.trash()*50000 - tetris.gameover*1000000
        #Weightedscore = 1000000 + -(20-self.maxRow)*25000 +self.yfactor*25000 + tetris.erasedLinedCount*tetris.erasedLinedCount*1000000 - (tetris.trash()-(20-self.maxRow)/4)*40000 - tetris.gameover*1000000
        #Weightedscore = 1000000 + -(20-self.maxRow)*(20-self.maxRow)*1000 +self.yfactor*10000 + tetris.erasedLinedCount*tetris.erasedLinedCount*1000000 - (tetris.trash()-(20-self.maxRow)/4)*40000 - tetris.gameover*1000000
        Weightedscore = 1000000 + -(20-self.maxRow)*25000 +self.yfactor*25000 + tetris.erasedLinedCount*tetris.erasedLinedCount*1000000 - (tetris.trash()-(20-self.maxRow)/4)*40000 - tetris.gameover*1000000
        if Weightedscore == self.maxScoreChoice[2]:
            if randint (0,1) == 0:
                nextscore = Weightedscore

        if Weightedscore> self.maxScoreChoice[2]:

            nextscore = Weightedscore

            self.maxScoreChoice = [r,x,nextscore, direction]

    
    def Simulatemovement (self, tetris, x):
        #Movimientos a la derecha

        NumberofMovements = 0
        NumberOfRotations = 0

        self.playabletetris =  deepcopy(tetris)
        for NumberOfRotations in range (4):
            for NumberofMovements in range (8):
                self.playabletetris =  deepcopy(tetris)
                for CurrentNumberofRutations in range (NumberOfRotations):
                        self.playabletetris.rotate = True
                        self.playabletetris.tick()
                
                for CurrentNumberOfMovements in range (NumberofMovements):
                    self.playabletetris.dx = 1*x
                    self.playabletetris.tick()             
                        
                self.playabletetris.snap_down()
                self.yfactor = self.playabletetris.yfactor
                self.playabletetris.tick()  
                #self.playabletetris.tick()

                self.tetriserasedlines = self.playabletetris.erasedLinedCount

                self.setMaxScoreChoice( NumberOfRotations,NumberofMovements,self.playabletetris.score,x, self.playabletetris)


          
    def observe(self, tetris):
        if self.step  == 4:
            self.maxScoreChoice = [0, 0, 0, 1]
        
        l=1
        if self.step==2:
            self.playabletetris =  deepcopy(tetris)
            self.Simulatemovement(tetris, l)
        elif self.step ==1:
            self.playabletetris =  deepcopy(tetris)
            self.Simulatemovement(tetris, -l)
        elif self.step ==0:
            self.status = "moving" 
        self.step -=1

    def movement(self,tetrisinstance):
        if tetrisinstance.gameover:
            return
        if self.status == "thinking":
            self.observe (tetrisinstance)

        else:
            #rotation
            tetrisinstance.rotate = False
            if self.maxScoreChoice[0]> 0:
            #for h in range (self.maxScoreChoice[0]):
                tetrisinstance.rotate = True
                self.maxScoreChoice[0]-=1
            
            else:

                if self.maxScoreChoice[1]> 0:
                #for i in range (self.maxScoreChoice[1]):
                    print ("MaxScoreChoice elected: " + str(self.maxScoreChoice) )
                    tetrisinstance.dx = 1*self.maxScoreChoice[3]
                    self.maxScoreChoice[1]-=1
                    #tetrisinstance.tick()

                
                if self.maxScoreChoice[0] == 0 and self.maxScoreChoice[1]== 0:
                    if self.movementCount <=0:                
                        tetrisinstance.anim_limit=100
                        self.movementCount = 4
                    else:
                        self.movementCount-= randint(1, 2)   
                    #tetrisinstance.anim_limit = 100   
                    if self.tempScore != tetrisinstance.score:
                        self.tempScore = tetrisinstance.score
                        self.status = "thinking"
                        self.step = 4
            tetrisinstance.tick()


        

