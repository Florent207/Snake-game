"""
----------------------------------------------------------------------------------------------------------------------
                                         GAME SNAKE WITH PYGAME ZERO
----------------------------------------------------------------------------------------------------------------------

This game is based on the features of PyGame Zero. There were many functions and methods for start the game like :
 - import additionnal modules
 - initialize firsts variables to create class
 - make speed of the game
 - make the snake
 - make game over
 - make additionnal food
 - make functions update() for make interactions in the game (directions, moves, ...)
 - realize draw() for make the first elements in the game (like background, snake, limits, ...)
 - initialize last variables that are chosen by the user
"""

"""======== IMPORT ADDITIONNAL MODULES ========"""
import pgzrun
import copy
import random
import sys
import os

"""======== INITIALIZE ENVIRONNEMENT ========"""
# details of environnement
# size of the  layout = 25*20(body size)+24(number of space)+2(line border) ! Has to be changed if SIZE and SPACE change in Snake class
WIDTH = 526
HEIGHT = 526
BORDER = Rect((0,0),(WIDTH, HEIGHT))
TITLE = 'Royal Python'
background = Actor('sand')
background.pos = 250, 250

# init first variables for directions/moves, use wall, increase speed and time of it, score
upIsPressed=False
downIsPressed=False
rightIsPressed=False
leftIsPressed=False
throughHimself=False 
crossWall=True
increaseSpeed=False
timeSpeedIncrease=5
score = 0

# step_mode for debug and dev
step_mode=False

"""======== INITIALIZE CLOCK ========"""
# this sets the speed of the game 
class Clock():
    def __init__(self,frequency):
        self.frequency=frequency
        self.inc=0
    def call(self):
        self.inc+=1
        if self.inc>=self.frequency*60:
            self.inc=0
            return True
        else:
            return False

"""======== INITIALIZE GAME OVER ========"""
class FinalScreen(Actor):
    def __init__(self,image):
        super().__init__(image)
        self.area=[]
        self.isWritten=False
        # positions for write GAME OVER on the final screen
        self.word=[(32,116),(32,137),(32,158),(32,179),(32,200),(53,200),(74,200),(95,200),(116,200),(53,116),(74,116),(95,116),(116,116),(116,158),(116,179),(95,158),(74,158),#Letter G
                   (158,116),(158,137),(158,158),(158,179),(158,200),(179,116),(200,116),(221,116),(242,116),(242,137),(242,158),(242,179),(242,200),(221,158),(200,158),(179,158),#letter A
                   (284,116),(305,116),(326,116),(347,116),(368,116),(284,137),(284,158),(284,179),(284,200),(368,137),(368,158),(368,179),(368,200),(326,137),(326,158),(326,179),(326,200),(404,116),#Lettre M
                   (410,116),(431,116),(452,116),(473,116),(494,116),(410,137),(410,158),(410,179),(410,200),(431,200),(452,200),(473,200),(494,200),(431,158),(452,158),(473,158),(494,158),#Letter E
                   (32,326),(32,347),(32,368),(32,389),(32,410),(53,326),(74,326),(95,326),(116,326),(116,347),(116,368),(116,389),(116,410),(53,410),(74,410),(95,410),#Letter O
                   (158,326),(158,347),(158,368),(242,326),(242,347),(242,368),(179,389),(200,410),(221,389),#Letter V
                   (284,326),(305,326),(326,326),(347,326),(368,326),(284,347),(284,368),(284,389),(284,410),(305,410),(326,410),(347,410),(368,410),(305,368),(326,368),(347,368),(368,368),#Letter E
                   (410,326),(410,347),(410,368),(410,389),(410,410),(431,326),(452,326),(473,326),(494,347),(494,368),(473,389),(494,410)]#Letter R
        self.areaToWrite=[]
        for x in range(int(Snake.SIZE/2)+1,WIDTH-int(Snake.SIZE/2),Snake.SIZE+1):#+1 just tu make a supplementra turn ,(11,515+1,21),Snake.SIZE/2+1,WIDTH-Snake.SIZE/2,Snake.SIZE+1
            for y in range(int(Snake.SIZE/2)+1,WIDTH-int(Snake.SIZE/2),Snake.SIZE+1):
                self.area.append((x,y))
        for z in self.word:
            if z in self.area:
                self.area.remove(z)
    
    # init draw for game over           
    def draw(self):
        self.addPos()
        for i in self.areaToWrite:
            self.pos=i
            super().draw()
            
    # write game over  
    def addPos(self):
        for i in range(20):# just to increase the frequency
            try:
                dummy=random.choice(self.area)
                self.areaToWrite.append(dummy)
                self.area.remove(dummy)
            except:
                pass

"""======== INITIALIZE FOOD ========"""
class Food(Actor):
    def __init__(self,image):
        super().__init__(image)
        self.area=[]
        for x in range(int(Snake.SIZE/2)+1,WIDTH-int(Snake.SIZE/2),Snake.SIZE+1):#+1 just tu make a supplementra turn ,(11,515+1,21),Snake.SIZE/2+1,WIDTH-Snake.SIZE/2,Snake.SIZE+1
            for y in range(int(Snake.SIZE/2)+1,WIDTH-int(Snake.SIZE/2),Snake.SIZE+1):
                self.area.append((x,y))
    
    def newPos(self,pos):
        newFoodPosList=copy.deepcopy(self.area)
        currentSnakePosList=copy.deepcopy(pos)
        
        for p in currentSnakePosList:
            if currentSnakePosList.count(p)>1: #Remove all the same position of the snake
                try:
                    i=0
                    while True:
                        currentSnakePosList.remove(p)
                        print('this one is removed :',p)
                        i+=1
                except (ValueError) as err:#end of the remove
                   print('issue with removing',err)
                   print('snake size:',len(snake.getPosList())-i)
                   pass

            if p in self.area:#Careful, if snake has 2 same position (i.e for debug mode). this function won't work properly ! It has been fixed with the code above
                try:
                    newFoodPosList.remove(p)
                except (ValueError) as err:
                    print('this one is alread removed', err)
                    pass#only no more place left for the food
       
        self.pos=newFoodPosList[random.randint(0,len(newFoodPosList)-1)]

"""======== INITIALIZE SNAKE ========"""
class Snake (Actor) :
    #snake is a head, body and tail
    #ATTRIBUTE : ANGLE,X,Y,IMAGE ¦¦ METHODE : DRAW(), Are the only things we will use on the parent Class "Actor"
    SIZE=20#20*20 pix is the snake "body segment"
    SPACE=1#is the space between each "body segment"
    DELTA=SIZE+SPACE
    
    def __init__(self,image,pos):
        super().__init__(image,pos)
        self.posList =[pos]
        self.headDirection='GR'#goes right
        self.dead=False
        self.ImFull=[]
    
    # add body to the snake when he eat
    def addSegment(self):
        x,y=self.getTailX(),self.getTailY()
        try :
            x_1,y_1=self.posList[-2][0],self.posList[-2][1]
        except:#snake has only one head
            if self.headDirection =='GR':
                x,y=self.getTailX()-Snake.DELTA,self.getTailY()
            elif self.headDirection =='GL':
                x,y=self.getTailX()+Snake.DELTA,self.getTailY()
            elif self.headDirection =='GU':
                x,y=self.getTailX(),self.getTailY()+Snake.DELTA
            elif self.headDirection =='GD':
                x,y=self.getTailX(),self.getTailY()-Snake.DELTA                  
        else :
            if x_1<x:
                x=self.getTailX()+Snake.DELTA
            elif x_1>x:
                x=self.getTailX()-Snake.DELTA
            elif y_1<y:
                y=self.getTailY()+Snake.DELTA
            elif y_1>y:
                y=self.getTailY()-Snake.DELTA      
        self.posList.append((x,y))
        
    #Add head pos and remove tail pos
    def updatePosList(self,pos):
        self.posList.insert(0,(pos));self.posList.pop()
    def getHeadPos(self):
        return self.posList[0]
    def getHeadX(self):
        return self.posList[0][0]
    def getHeadY(self):
        return self.posList[0][1]
    def getTailPos(self):
        return self.posList[-1]
    def getTailX(self):
        return self.posList[-1][0]
    def getTailY(self):
        return self.posList[-1][1]
    def getTailX_1(self):
        return self.posList[-2][0]
    def getTailY_1(self):
        return self.posList[-2][1]
    def getPosList(self):
        return self.posList
    def setHeadDir(self,dir_p):
        self.headDirection=dir_p
    def setHeadDirV2(self):
        if self.headDirection=='GR':
            self.angle=0
        elif self.headDirection=='GL':
            self.angle=180
        elif self.headDirection=='GU':
            self.angle=90
        elif self.headDirection=='GD':
            self.angle=-90
    def setAngle(self,x,y,x_1,y_1):
        if x_1<x:
            self.angle = 180
        elif x_1>x:
            self.angle = 0
        elif y_1<y:
            self.angle = 90
        elif y_1>y:
            self.angle = -90  
    def setTailDir(self):
        x,y,x_1,y_1=self.getTailX(),self.getTailY(),self.getTailX_1(),self.getTailY_1()
        self.setAngle(x,y,x_1,y_1)
    def setBodyDir(self,pos):
        x,y,x_1,y_1=pos[0],pos[1],self.posList[self.posList.index(pos)-1][0],self.posList[self.posList.index(pos)-1][1]
        self.setAngle(x,y,x_1,y_1)
    def isHead(self):
        super().__init__('head',self.pos)
    def isTail(self):
        super().__init__('tail',self.pos)
    def isBody(self):
        super().__init__('body',self.pos)
    def isBelly(self):
        super().__init__('belly',self.pos)
    def isHimDead(self):
        return self.dead
    def isDead(self):
        self.dead=True
    def isFoodEaten(self):
        return self.yummy

    def draw(self,foodPos):
        global score
        self.yummy=False
        
        for i in self.posList:
            if self.getHeadPos() in self.posList[1:]:#snake touched himself , let on the FOR for debuf purpose with "throughHimself"
                if not throughHimself:#for debug purpose
                    self.dead=True
            self.pos=i
            if self.collidepoint(foodPos):#snake eat food
                self.addSegment()
                self.yummy=True
                self.ImFull.append(i)
                sounds.miam.play()
                score += 1
            if i==self.getHeadPos():
                self.isHead()
                self.setHeadDirV2()
            elif i==self.getTailPos():
                self.isTail()
                self.setTailDir()
            else:
                if i in self.ImFull:
                    self.isBelly()
                    self.setBodyDir(i)
                    if i==(self.getTailX_1(),self.getTailY_1()):
                        self.ImFull.remove(i)
                else:
                    self.isBody()
                    self.setBodyDir(i)
            super().draw()   

"""======== INITIALIZE MOVES ========"""
def manageKeyboard(doIt):
    global upIsPressed
    global downIsPressed
    global rightIsPressed
    global leftIsPressed
    global crossWall
    
    # sets the direction
    if (keyboard.right and not keyboard.up and not keyboard.down and not keyboard.left and not leftIsPressed):
        rightIsPressed=True;leftIsPressed=False;upIsPressed=False;downIsPressed=False
        
    if (keyboard.left and not keyboard.up and not keyboard.down and not keyboard.right and not rightIsPressed):
        rightIsPressed=False;leftIsPressed=True;upIsPressed=False;downIsPressed=False
   
    if (keyboard.up and not keyboard.down and not keyboard.right and not keyboard.left and not downIsPressed):
        rightIsPressed=False;leftIsPressed=False;upIsPressed=True;downIsPressed=False
    
    if (keyboard.down and not keyboard.up and not keyboard.right and not keyboard.left and not upIsPressed):
        rightIsPressed=False;leftIsPressed=False;upIsPressed=False;downIsPressed=True
   
    # sets moves according to the direction    
    if rightIsPressed and doIt :
        if snake.getHeadX()+Snake.DELTA>WIDTH-1:
            if not crossWall:
                snake.isDead()
            else:
                snake.updatePosList((Snake.SIZE/2+1,snake.getHeadY()))# +1 is the border line
                sounds.wall.play()
        else:
            snake.updatePosList((snake.getHeadX()+Snake.DELTA,snake.getHeadY()))
        snake.setHeadDir('GR')
                    
    if leftIsPressed and doIt:
        if snake.getHeadX()-Snake.DELTA<1:#1 is the border line
            if not crossWall:
                snake.isDead()
            else:
                snake.updatePosList((WIDTH-Snake.SIZE/2-1,snake.getHeadY()))# +1 is the border line
                sounds.wall.play()
        else:
            snake.updatePosList((snake.getHeadX()-Snake.DELTA,snake.getHeadY()))
        snake.setHeadDir('GL')
      
    if upIsPressed and doIt:     
        if snake.getHeadY()-Snake.DELTA<1:# +1 is the border line
            if not crossWall:
                snake.isDead()
            else:
                snake.updatePosList((snake.getHeadX(),HEIGHT-Snake.SIZE/2-1))
                sounds.wall.play()
        else:
            snake.updatePosList((snake.getHeadX(),snake.getHeadY()-Snake.DELTA))
        snake.setHeadDir('GU')
            
    if (keyboard.down and not keyboard.up and not keyboard.right and not keyboard.left and not upIsPressed or downIsPressed)and doIt:
        if snake.getHeadY()+Snake.DELTA>HEIGHT-1:# +1 is the border line
            if not crossWall:
                snake.isDead()
            else:
                snake.updatePosList((snake.getHeadX(),Snake.SIZE/2+1))
                sounds.wall.play()
        else:
            snake.updatePosList((snake.getHeadX(),snake.getHeadY()+Snake.DELTA))
        snake.setHeadDir('GD')
        
"""======== INITIALIZE LAST VARIABLES AND ACTORS ========"""
# last variables
gameOver=FinalScreen('explosion')
snake = Snake('body',(263,263))#it can be any other images, it does not matter,1(line border)+10(body/2)+12*20(body size)+12.This is the center
food = Food('food')
food.newPos(snake.posList)
final=False # for sound at the final screen
GUI_DONE = 0 # variable user's choices

# actors for begin screen
easy = Actor('easy', (263, 105))
medium = Actor('medium', (263, 210))
hard = Actor('hard', (263, 315))
expert = Actor('expert', (263, 420))
use_wall = Actor('use_wall', (263, 175))
no_use_wall = Actor('no_use_wall', (263, 350))

# it's for initialize speed's parameter
clock1=Clock(0.1) #0.05sec pulse --> this is to choose speed in function of mode
clock2=Clock(5)#5sec seconds --> this is the time between incresease of speed

"""======== INITIALIZE UPDATE() ========"""    
def update():
    global frequency
    global step_mode
    global GUI_DONE
    global crossWall
    
    if not step_mode:
        if GUI_DONE == 2 or GUI_DONE == 3:
            if clock2.call():
                clock1.frequency=clock1.frequency-clock1.frequency*0.1#has to be change dependen the mode choosen 
        manageKeyboard(clock1.call())
        
"""======== INITIALIZE DRAW() ========"""
#is called after each update, clock or inputs ("HOOK MANAGE EVENT")
def draw():
    pass
    global score
    global final
    global GUI_DONE
    
    # begin game
    if GUI_DONE == 2 or GUI_DONE == 3:
        screen.clear()
        background.draw()
        screen.draw.rect(BORDER,(0,0,0))
        
    # final screen and game over
    if snake.isHimDead():
        if final==False:
            sounds.dead.play()
            final=True
        sounds.wall.stop()
        gameOver.draw()
        screen.draw.text("Final score = " + str(score), (186,235), color=(224, 224, 224), fontsize=32)
        screen.draw.text("Press Q to quit or press R to restart", (78,275), color=(255, 255, 255), fontsize=32)
        if keyboard.q:
            print('GG! See you later!')
            sys.exit(0)
        if keyboard.r:
            print('One more chance? Ok!')
            os.execv(sys.executable, ['Snake_Game.py'] + sys.argv)
    
    # first begin screen for choose level of difficulty
    elif GUI_DONE == 0:
        screen.fill((0,0,0))
        easy.draw()
        medium.draw()
        hard.draw()
        expert.draw()
    
    # second begin screen for choose to use wall or not
    elif GUI_DONE == 1:
        screen.fill((0,0,0))
        no_use_wall.draw()
        use_wall.draw()
    
    # draw game's screen
    else:
        screen.draw.text('Score : ' + str(score), (15,10) , color=(0,0,0), fontsize=30)
        food.draw()
        snake.draw(food.pos)    
        if snake.isFoodEaten():
            food.newPos(snake.posList)

"""======== INIT GAME BY USER ========"""
def on_mouse_down(pos):
    global frequency
    global GUI_DONE
    global crossWall
    global clock1
    
    # make buttons for choose level of difficulty
    if easy.collidepoint(pos):
        sounds.button.play()
        clock1=Clock(0.15)
        GUI_DONE= 1
    if medium.collidepoint(pos):
        sounds.button.play()
        clock1=Clock(0.12)
        for i in range(4):
            snake.addSegment()
        GUI_DONE= 1
    if hard.collidepoint(pos):
        sounds.button.play()
        clock1=Clock(0.08)
        for i in range(7):
            snake.addSegment()
        GUI_DONE= 1
    if expert.collidepoint(pos):
        sounds.button.play()
        clock1=Clock(0.05)
        for i in range(12):
            snake.addSegment()
        GUI_DONE= 1
        
    # make buttons for choose to use wall or not
    if no_use_wall.collidepoint(pos):
        sounds.button.play()
        crossWall=False
        GUI_DONE= 2
    if use_wall.collidepoint(pos):
        sounds.button.play()
        crossWall=True
        GUI_DONE= 3
        
"""======== INIT STEPMODE FOR DEBUG ========"""
def on_key_down(key,mod,unicode):
    global step_mode
    if step_mode :
        manageKeyboard(True)

"""======== FUNCTIONS TO START THE GAME ========"""
sounds.hello.play()    
pgzrun.go()