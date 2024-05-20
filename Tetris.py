from copy import deepcopy
from random import choice, randrange, randint, Random
import pygame

W, H = 10, 20
TILE = 45
GAME_RES = W * TILE, H * TILE
RES = 750, 940
FPS = 60


       

class tetris():
    def __init__(self):
        self.tetriserasedlines, self.yfactor = 0, 0
        self.placeSound= False
        self.lineErased= False
        self.loseSound= False
        
        self.trashAmount = 0
        self.snap = False
        self.gameover = False
        self.erasedLinedCount = 0
        self.randomizer = Random()
        self.randomizer.seed(41)
        self.dx, self.rotate = 0, False
        self.bag = {}
        self.figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
                    [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                    [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                    [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                    [(0, 0), (0, -1), (0, 1), (-1, -1)],
                    [(0, 0), (0, -1), (0, 1), (1, -1)],
                    [(0, 0), (0, -1), (0, 1), (-1, 0)]]
        self.field = [[0 for i in range(W)] for j in range(H)]
        self.figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in self.figures_pos]
        self.anim_count, self.anim_speed, self.anim_limit = 0, 60, 2000
        self.figure, self.next_figure = deepcopy(self.randomizer.choice(self.figures)), deepcopy(self.randomizer.choice(self.figures))
        self.score, self.lines = 0, 0
        self.scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}
    def check_borders(self):
        for i in range (4):
            if self.figure[i].x < 0 or self.figure[i].x > W - 1:
                return False
            elif self.figure[i].y > H - 1 or self.field[self.figure[i].y][self.figure[i].x]:
                return False
        return True
    
    def MakeDoubleBag(self):
        """Makes a bag of 2 of each tetromino type."""
        for i in self.tetromino_type_list:
            self.bag.update({i: 2})


    def Choose(self):
        """Returns a choice from the bag, and removes that block from the bag."""
        if self.bag == {}:
            self.MakeDoubleBag()
        lst = [x for x in self.bag.keys()]
        choice = self.randomizer.choices(lst, k=1)[0]
        if self.bag.get(choice) == 1:
            self.bag.pop(choice)
        else:
            self.bag.update({choice: self.bag.get(choice) - 1})
        return choice

    def MakeDoubleBag(self):
        for i in range (7):
            self.bag.update({i: 2})

    def initialize(self, seed):
        for i in range(W):
            self.gameover = False
            self.randomizer.seed(seed)
            self.field = [[0 for i in range(W)] for i in range(H)]
            self.figure, self.next_figure = deepcopy(self.randomizer.choice(self.figures)), deepcopy(self.randomizer.choice(self.figures))
            self.anim_count, self.anim_speed, self.anim_limit = 0, 60, 2000
            self.score = 0
            self.grace_timer = 5

    def trash (self): #Calcula Cuantas basura hay en el entorno de juego
        count = 0
        bandtrash = False
        for column in range( W - 1, -1, -1):
            for i in range(H):
                if self.field[i][column]:
                    bandtrash = True
                    
                elif bandtrash:
                    count += 1
            bandtrash = False
                    
        self.trashAmount = count
        return self.trashAmount
    def get_record():
        try:
            with open('record') as f:
                return f.readline()
        except FileNotFoundError:
            with open('record', 'w') as f:
                f.write('0')

    def set_record(record, score):
        rec = max(int(record), score)
        with open('record', 'w') as f:
            f.write(str(rec))
    def calculateNumberOfRows(self): #Calcula el numero de columnas que tengan almenos un bloque
        line, lines = H - 1, 0
        maxRow = 20
        for row in range(H - 1, -1, -1):
            count = 0
            for i in range(W):
                if self.field[row][i]:
                    count += 1
            if count !=0:
                if maxRow >= row:
                    maxRow = row
        return maxRow

    def horizontal_movement(self):
        figure_old = deepcopy(self.figure)
        for i in range(4):
            self.figure[i].x += self.dx
            if  not self.check_borders():
                self.figure = deepcopy(figure_old)
                break
        self.dx = 0
    def getNextPiece(self):
        #self.next_figure = deepcopy(self.figures[self.randomizer.randint(4,6)])
        self.next_figure = deepcopy(self.figures[self.Choose()])
        self.placeSound = True

    def vertical_movement(self):
        if self.snap == True:
            self.snap = False
            return
        figure_old = deepcopy(self.figure)
        self.anim_count += self.anim_speed
        if self.anim_count > self.anim_limit and self.grace_timer <= 0:
            self.anim_count = 0
            self.anim_speed +=0.1
            for i in range(4):
                self.figure[i].y += 1
                if not self.check_borders():
                    self.score +=10
                    for i in range(4):
                        self.field[figure_old[i].y][figure_old[i].x] = pygame.Color("white")
                    self.figure = self.next_figure
                    self.grace_timer = 10
                    self.getNextPiece()
                    #self.next_figure = deepcopy(self.randomizer.choice(self.figures))

                    break
        self.anim_limit = 2000
    def snap_down (self):
        self.yfactor = 0
        while True and not self.gameover:
            self.yfactor+=1
            
            figure_old = deepcopy(self.figure)
            for i in range(4):
                self.figure[i].y += 1
                if not self.check_borders():
                    self.score +=10
                    for i in range(4):
                        self.field[figure_old[i].y][figure_old[i].x] = pygame.Color("white")
                        
                    self.figure = self.next_figure
                    self.getNextPiece()
                    self.snap = True
                    #self.placeSound.stop()
                    #self.placeSound.play()                       
                    return 
                
    def rotation_movement (self):
        center = self.figure[0]
        figure_old = deepcopy(self.figure)
        if self.rotate:
            for i in range(4):
                x = self.figure[i].y - center.y
                y = self.figure[i].x - center.x
                self.figure[i].x = center.x - x
                self.figure[i].y = center.y + y
                if not self.check_borders():
                    self.figure = deepcopy(figure_old)
                    break
        self.rotate = False
    def tick(self):
        self.erasedLinedCount = 0
        self.grace_timer -=1
        if  self.gameover != True:
            
            #Movimiento Horizontal
            self.horizontal_movement()

            #Movimiento vertical
            
            self.vertical_movement()
            #self.snap_down(figure_old)

            #Funcion para rotar el objeto

            self.rotation_movement()           

            #Verificador de Line y puntuador
            
            line, lines = H - 1, 0
            for row in range(H - 1, -1, -1):
                count = 0
                for i in range(W):
                    if self.field[row][i]:
                        count += 1
                    self.field[line][i] = self.field[row][i]
                #   if count !=0:
                #    print ("Cantidad de Cuadros en la Linea: "+ str(row)  + " Es: "+ str(count))
                if count < W:
                    line -= 1
                    
                else:
                    self.anim_speed += 3
                    self.lineErased = True
                    lines += 1
                    self.erasedLinedCount +=1
                
            self.score += self.scores[lines]
            for i in range(W):
                if self.field[0][i]:
                    #set_record(record, score)
                    
                    self.loseSound = True
                    self.gameover = True
