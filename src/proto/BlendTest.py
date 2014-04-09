#! /usr/bin/env python

from __future__ import print_function

from PyQt4 import QtCore,QtGui
from PyQt4.QtOpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *

import time
import numpy
import math
import os, sys
import Texture

def distance(x1,y1,x2,y2):
  dx = x1 - x2
  dy = y1 - y2
  return math.sqrt(dx*dx + dy*dy)

class BlendGL(QGLWidget):
    def __init__(self, parent):
      QGLWidget.__init__(self, parent)
      self.setMouseTracking(True)
      self.isPressed = False
      self.oldx = self.oldy = 0
      self.nearest = -1
      self.startTime = float(time.time())
      self.warpWidth = 512
      self.warpHeight = 512
      self.border = 0.0
      self.texID = 0
      self.brushSize = 30.0
      self.brushSoftness = 1.0
      self.brushMode = False
      self.brushImage = None
      self.updateBrushImage()
      self.leftOverDistance = 0

    def updateBrushImage(self):
      size = int(math.ceil(self.brushSize))
      self.brushImage = numpy.zeros(size*size,numpy.uint8)
      r = self.brushSize * 0.5
      innerRadius = self.brushSoftness * ( - r) + r

      for x in range(0,size):
        for y in range(0,size):
          d = distance(x,y,r,r)
          v = (d - innerRadius) / (r - innerRadius)
          if v < 0.0: v = 0.0
          if v > 1.0: v = 1.0
          self.brushImage[y*size+x] = v * 255

    def paintGL(self):  
      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
      glDisable( GL_DEPTH_TEST )
      glDisable( GL_CULL_FACE ) 

      if self.texID == 0: return

      glLoadIdentity()
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()
      
      left, right, top, bottom = self.viewRect()
 
      gluOrtho2D(left,right,top,bottom)

      glMatrixMode(GL_MODELVIEW)
      glLoadIdentity()

      glBegin(GL_QUADS)
      glColor4f(1.0,1.0,1.0,1.0)
      glTexCoord2f(0.0, 0.0); glVertex2f(-0.5,-0.5)
      glTexCoord2f(1.0, 0.0); glVertex2f(0.5,-0.5) 
      glTexCoord2f(1.0, 1.0); glVertex2f(0.5,0.5)
      glTexCoord2f(0.0, 1.0); glVertex2f(-0.5,0.5)
      glEnd()


      glEnable(GL_TEXTURE_2D)
      glBindTexture(GL_TEXTURE_2D, self.texID)
      glColor4f(0.0,0.0,0.0,1.0)
      glBlendFunc (GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
      glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)   
      glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S,GL_CLAMP_TO_EDGE);
      glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T,GL_CLAMP_TO_EDGE);
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
      self.updateTex()

      glBegin(GL_QUADS)
      #glColor4f(1.0,1.0,1.0,1.0)
      glTexCoord2f(0.0, 0.0); glVertex2f(-0.5,-0.5)
      glTexCoord2f(1.0, 0.0); glVertex2f(0.5,-0.5) 
      glTexCoord2f(1.0, 1.0); glVertex2f(0.5,0.5)
      glTexCoord2f(0.0, 1.0); glVertex2f(-0.5,0.5)
      glEnd()
      glBindTexture(GL_TEXTURE_2D, 0)
 
      glColor4f(1.0,1.0,1.0,1.0)
      posx,posy = self.screenPos()

      glEnable(GL_BLEND);
      glBlendFunc(GL_ONE_MINUS_DST_COLOR, GL_ZERO); 
      glBegin(GL_LINE_LOOP)
      n = 16
      r = self.brushSize*0.5 / self.warpWidth
      for i in range(0,n):
        glVertex2f(posx+
            r*math.cos(i/float(n)*math.pi*2),posy+
            r*math.sin(i/float(n)*math.pi*2) * (self.warpWidth/float(self.warpHeight)) )
      glEnd()


      self.update()
      #glFlush()

    def resizeGL(self, widthInPixels, heightInPixels):
      glViewport(0, 0, widthInPixels, heightInPixels)

    def viewRect(self):
      warpAspect = float(self.warpWidth) / self.warpHeight      
      viewAspect = float(self.width()) / self.height()
      b = self.border * 0.5
      left, right, top, bottom = -0.5 - b,0.5 + b,-0.5 - b,0.5 + b

      if warpAspect > viewAspect:
        top *= warpAspect / viewAspect
        bottom *=  warpAspect / viewAspect
      else:
        left *= viewAspect / warpAspect
        right *= viewAspect / warpAspect
      return left, right, top, bottom
      

    def initializeGL(self):
      glClearColor(0.0, 0.0, 0.0, 1.0)
      glClearDepth(1.0)
      glEnable(GL_TEXTURE_2D)
      glEnable(GL_BLEND)
      self.texID = glGenTextures(1)
      self.texData = numpy.zeros((self.warpWidth*self.warpHeight),numpy.uint8)

      glBindTexture(GL_TEXTURE_2D, self.texID)
      glPixelStorei(GL_UNPACK_ALIGNMENT,1)
      glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
      glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
      self.updateTex()
      glBindTexture(GL_TEXTURE_2D,0)

    def updateTex(self):
      glTexImage2D(
          GL_TEXTURE_2D, 0, GL_ALPHA, self.warpWidth, self.warpHeight, 0,
          GL_ALPHA, GL_UNSIGNED_BYTE, self.texData)

    def mouseMoveEvent(self, e):
      if self.isPressed:
        self.leftOverDistance = self.drawLine(self.oldx,self.oldy,e.x(),e.y(),self.leftOverDistance)
      self.oldx = e.x()
      self.oldy = e.y()     
      self.update()

    def keyPressEvent(self,e):
      self.update()
      if e.key() == QtCore.Qt.Key_Left:
        self.brushSoftness -= 0.01
      elif e.key() == QtCore.Qt.Key_Right:
        self.brushSoftness += 0.01
      elif e.key() == QtCore.Qt.Key_Up:
        self.brushSize += 1
      elif e.key() == QtCore.Qt.Key_Down:
        self.brushSize -= 1
      elif e.key() == QtCore.Qt.Key_Space:
        self.brushMode = not self.brushMode

      self.updateBrushImage()
      print(self.brushSize,self.brushSoftness)

    def mousePressEvent(self, e):
      self.isPressed = True
      p1x,p1y = self.pixelPos(e.x(),e.y())
      self.leftOverDistance = 0.0
      self.manipulatePixel(p1x,p1y)
      self.oldx = e.x()
      self.oldy = e.y()
      self.update()


#int innerRadius = (int)ceil(mSoftness * (0.5 - mRadius) + mRadius);
#int outerRadius = (int)ceil(mRadius);

#float alphaStep = 1.0 / (outerRadius - innerRadius + 1);

    def drawLine(self,p1x,p1y,p2x,p2y,leftOverDistance):
      p1x,p1y = self.pixelPos(p1x,p1y)
      p2x,p2y = self.pixelPos(p2x,p2y)
      # Anything less that half a pixel is overkill and could hurt performance.
      spacing = self.brushSize / 10.0
      if spacing < 0.5 : spacing = 0.5

      deltaX = p2x - p1x;
      deltaY = p2y - p1y;
      dist = distance(p1x,p1y,p2x,p2y)
      stepX = 0.0
      stepY = 0.0
      if dist > 0.0 :
		    invertDistance = 1.0 / dist
		    stepX = deltaX * invertDistance
		    stepY = deltaY * invertDistance
        
      offsetX = 0.0
      offsetY = 0.0
      totalDistance = leftOverDistance + dist
    	# While we still have distance to cover, stamp
      while totalDistance >= spacing :
        if leftOverDistance > 0:
			    offsetX += stepX * (spacing - leftOverDistance)
			    offsetY += stepY * (spacing - leftOverDistance)
			    leftOverDistance -= spacing
        else:
			    offsetX += stepX * spacing
			    offsetY += stepY * spacing
        self.manipulatePixel(p1x + offsetX,p1y + offsetY)
			
        totalDistance -= spacing
      return totalDistance
	
    def manipulatePixel(self,x,y):
      r = self.brushSize*0.5
      size = int(math.ceil(self.brushSize))
      
      for i in range(0,size):
        for j in range(0,size):
          posx = int(i + x - r)
          posy = int(j + y - r)
          if (posx < 0) or (posx >= self.warpWidth): continue
          if (posy < 0) or (posy >= self.warpHeight): continue
          idx = posy*self.warpWidth+posx
          v = self.brushImage[j*size + i]/255.0
          if self.brushMode:
            pix= self.texData[idx] * v
          else:
            pix= 255.0 - 255.0*v + self.texData[idx] * v
          self.texData[idx] = pix 

    def mouseReleaseEvent(self, e):
      self.isPressed = False
      self.leftOverDistance = 0.0
      self.update()


    def toScreenPos(self,x,y):
      left, right, top, bottom = self.viewRect()
      width = right - left
      height = bottom - top
      return ((float(x) / self.width() - 0.5) * width,(1.0 - float(y) / self.height() - 0.5) * height)

    def screenPos(self):
      return self.toScreenPos(self.oldx,self.oldy)
    
    def pixelPos(self,px,py):
      x,y = self.toScreenPos(px,py)
      return (int(float(x+0.5)*self.warpWidth),int(float(y+0.5)*self.warpHeight))
    


if __name__ == '__main__': 
  app = QtGui.QApplication(['WarpTest'])  

  window = BlendGL(None)
  window.show()
  sys.exit(app.exec_())

