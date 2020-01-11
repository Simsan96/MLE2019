# coding: utf8
import sys
import time
import math

try:
    import numpy as np
except:
    print("ERROR: Numpy not installed properly.")
    sys.exit()
try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
except:
    print("ERROR: PyOpenGL not installed properly.")
    sys.exit()

'''
INSTALLATION:
-----------------------------------------
unter anaconda (python 3.6):
    conda install numpy
    conda install freeglut
    conda install pyopengl
    conda install pyopengl-accelerate

(bei fehlenden Bibliotheken googeln)

Ausführung:
    start anaconda prompt
    navigiere in den Game Ordner
    tippe: python A5.py
-----------------------------------------
'''


class GameGL(object):
    config = None

    def __init__(self, config=None):
        self.config = config

    '''
    Is needed for the OpenGL-Library because standard strings are not allowed.
    '''

    def toCString(self, string):
        return bytes(string, "ascii")


class BasicGame(GameGL):
    windowName = "PingPong"
    # 30px
    pixelSize = 30

    xBall = 5
    yBall = 6
    xV = 1
    yV = 1
    xPaddle = 5
    score = 0

    xMax = 11
    yMax = 10
    xBallMax = xMax
    yBallMax = yMax
    xPaddleMax = 9
    maxV = 2



    def __init__(self, name, width=360, height=360):
        super
        self.windowName = name
        self.width = width
        self.height = height

    def keyboard(self, key, x, y):
        # ESC = \x1w
        if key == b'\x1b':
            sys.exit(0)

    def display(self, action, train=False):
        # init reward
        reward = 0

        if not train:
            # clear the screen
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # reset position
            glLoadIdentity()
            glViewport(0, 0, self.width, self.height)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            glOrtho(0.0, self.width, 0.0, self.height, 0.0, 1.0)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()

        # Paddle
        if action == 0:
            self.xPaddle -= 1  # Move left
        if action == 2:
            self.xPaddle += 1  # Move right
        # don't allow puncher to leave the pitch
        if self.xPaddle < 0:
            self.xPaddle = 0
        if self.xPaddle > self.xPaddleMax:
            self.xPaddle = self.xPaddleMax

        self.xBall += self.xV
        self.yBall += self.yV
        # change direction of ball if it's at wall
        if (self.xBall > self.xMax or self.xBall < 1):
            self.xV = -self.xV
        if (self.yBall > self.yMax or self.yBall < 1):
            self.yV = -self.yV
        # check whether ball on bottom line
        if self.yBall == 0:
            # check whether ball is at position of player
            if (self.xPaddle == self.xBall
                    or self.xPaddle == self.xBall - 1
                    or self.xPaddle == self.xBall - 2):
                reward += 1
            else:
                reward -= 1
                self.score += 1  # Recording the COMPUTER's score

        if not train:
            # repaint
            self.drawBall()
            self.drawComputer()
            # timeout of 100 milliseconds
            time.sleep(0.001)
            glutSwapBuffers()

        return reward

    def start(self, train=False):
        if not train:
            glutInit()
            glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
            glutInitWindowSize(self.width, self.height)
            glutInitWindowPosition(100, 100)
            glutCreateWindow(self.toCString(self.windowName))
            glutDisplayFunc(self.display)
            glutReshapeFunc(self.onResize)
            glutIdleFunc(self.display)
            glutKeyboardFunc(self.keyboard)

    def updateSize(self):
        self.width = glutGet(GLUT_WINDOW_WIDTH)
        self.height = glutGet(GLUT_WINDOW_HEIGHT)

    def onResize(self, width, height):
        self.width = width
        self.height = height

    def drawBall(self, width=1, height=1, x=5, y=6, color=(0.0, 1.0, 0.0)):
        x = self.xBall
        y = self.yBall
        xPos = x * self.pixelSize
        yPos = y * self.pixelSize
        # set color
        glColor3f(color[0], color[1], color[2])
        # start drawing a rectangle
        glBegin(GL_QUADS)
        # bottom left point
        glVertex2f(xPos, yPos)
        # bottom right point
        glVertex2f(xPos + (self.pixelSize * width), yPos)
        # top right point
        glVertex2f(xPos + (self.pixelSize * width), yPos + (self.pixelSize * height))
        # top left point
        glVertex2f(xPos, yPos + (self.pixelSize * height))
        glEnd()


    def drawComputer(self, width=3, height=1, x=0, y=0, color=(1.0, 0.0, 0.0)):
        x = self.xPaddle
        xPos = x * self.pixelSize
        # set a bit away from bottom
        yPos = y * self.pixelSize  # + (self.pixelSize * height / 2)
        # set color
        glColor3f(color[0], color[1], color[2])
        # start drawing a rectangle
        glBegin(GL_QUADS)
        # bottom left point
        glVertex2f(xPos, yPos)
        # bottom right point
        glVertex2f(xPos + (self.pixelSize * width), yPos)
        # top right point
        glVertex2f(xPos + (self.pixelSize * width), yPos + (self.pixelSize * height / 4))
        # top left point
        glVertex2f(xPos, yPos + (self.pixelSize * height / 4))
        glEnd()


#if __name__ == '__main__':
 #   game = BasicGame("PingPong")
  #  game.start()
