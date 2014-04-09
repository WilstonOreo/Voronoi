#!/usr/bin/env python
#
"""
    This file is part of DomeSimulator.

    DomeSimulator is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    DomeSimulator is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with DomeSimulator.  If not, see <http://www.gnu.org/licenses/>.

    DomeSimulator is free for non-commercial use. If you want to use it 
    commercially, you should contact the author 
    Michael Winkelmann aka Wilston Oreo by mail:
    me@wilstonoreo.net
"""

from __future__ import print_function

from MyGeom import Point3D, Vector3D, Matrix4x4

from PyQt4 import QtCore,QtGui
from PyQt4.QtOpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math
import time
import os

from array import array

try:
    from PIL.Image import open as ImageOpen
except ImportError, err:
    from Image import open as ImageOpen

from Base import *

class WarpGrid:
  def __init__(self,subdivX,subdivY):
    self.shape = (subdivX,subdivY)
    self.points = list()
    self.selectedPoints = set()
    self.resize(subdivX,subdivY)

  def resize(self,subdivX,subdivY):
    self.points[:] = []
    for y in range(0,subdivY):
      for x in range(0,subdivX):
        self.points.append((float(x)/(subdivX-1)-0.5,float(y)/(subdivY-1)-0.5))

    self.selectedPoints.add(7)

  def getNearest(self,x,y):
    nearestDist = 100000.0
    nearestIdx = 0
    idx = 0
    for point in self.points:
      dist = self.pointDist(point,(x,y))
      if dist < nearestDist:
        nearestIdx = idx
        nearestDist = dist 
      idx += 1
    return nearestIdx

  def pointDist(self,a,b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return dx * dx + dy * dy

  def getPoint(self,x,y):
    return self.points[y*self.shape[0]+x]

  def draw(self):
    glColor4f(0.0,0.0,1.0,1.0)
    glBegin(GL_LINES)
    for y in range(0,self.shape[1]-1):
      for x in range(0,self.shape[0]-1):
        p0 = self.getPoint(x,y)
        px = self.getPoint(x+1,y)
        py = self.getPoint(x,y+1)
        glVertex2f(p0[0],p0[1])
        glVertex2f(px[0],px[1])
        glVertex2f(p0[0],p0[1])
        glVertex2f(py[0],py[1])
    for y in range(0,self.shape[1]-1):
        p0 = self.getPoint(self.shape[1]-1,y)
        py = self.getPoint(self.shape[1]-1,y+1)
        glVertex2f(p0[0],p0[1])
        glVertex2f(py[0],py[1])
    for x in range(0,self.shape[0]-1):
        p0 = self.getPoint(x,self.shape[0]-1)
        px = self.getPoint(x+1,self.shape[0]-1)
        glVertex2f(p0[0],p0[1])
        glVertex2f(px[0],px[1])
    glEnd()

    glPointSize(10.0) 
    glBegin(GL_POINTS)
    idx = 0
    for point in self.points:
      glColor4f(1.0,1.0,1.0,1.0)
      for selPoint in self.selectedPoints:
        if idx == selPoint: 
          glColor4f(1.0,0.0,0.0,1.0)
      glVertex2f(point[0],point[1])
      idx += 1
    glEnd()



class WarpGLWidget(QGLWidget):
    def __init__(self, parent):
      QGLWidget.__init__(self, parent)
      self.setMouseTracking(True)
      self.isPressed = False
      self.oldx = self.oldy = 0
      self.warpGrid = WarpGrid(5,5)
      self.startTime = float(time.time())
      self.setAutoBufferSwap(True)
      self.warpWidth = 1024
      self.warpHeight = 768
      self.viewWidth = 1024
      self.viewHeight = 1024
      self.border = 0.0

    def paintGL(self): 
      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
      glDisable( GL_DEPTH_TEST )

      glLoadIdentity()
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()
      
      left, right, top, bottom = self.viewRect()
 
      gluOrtho2D(left,right,top,bottom)

      glMatrixMode(GL_MODELVIEW)
      glLoadIdentity()

      self.warpGrid.draw()
      self.update()

    def resizeGL(self, widthInPixels, heightInPixels):
      self.viewWidth = widthInPixels
      self.viewHeight = heightInPixels
      glViewport(0, 0, widthInPixels, heightInPixels)

    def initializeGL(self):
      glClearColor(0.0, 0.0, 0.0, 1.0)

    def viewRect(self):
      warpAspect = float(self.warpWidth) / self.warpHeight      
      viewAspect = float(self.viewWidth) / self.viewHeight
      b = self.border * 0.5
      left, right, top, bottom = -0.5 - b,0.5 + b,-0.5 - b,0.5 + b

      if warpAspect > viewAspect:
        top *= warpAspect / viewAspect
        bottom *=  warpAspect / viewAspect
      else:
        left *= viewAspect / warpAspect
        right *= viewAspect / warpAspect
      return left, right, top, bottom
      

    
    def mouseMoveEvent(self, mouseEvent):
        left, right, top, bottom = self.viewRect()
        width = right - left
        height = bottom - top
        dx = float(mouseEvent.x() - self.oldx) / self.width() * width
        dy = float(mouseEvent.y() - self.oldy) / self.height() * height
        if self.isPressed:
          for selIdx in self.warpGrid.selectedPoints:
            selPoint = self.warpGrid.points[selIdx]
            x = selPoint[0] + dx 
            y = selPoint[1] - dy 
            self.warpGrid.points[selIdx] = (x,y)
 
        self.oldx = mouseEvent.x()
        self.oldy = mouseEvent.y()        

        self.update()

    def keyPressEvent(self,e):
        for selIdx in self.warpGrid.selectedPoints:
          selPoint = self.warpGrid.points[selIdx]
          x = selPoint[0]
          y = selPoint[1] 
          if e.key() == QtCore.Qt.Key_Left:
            x -= 1.0 / self.width()
          if e.key() == QtCore.Qt.Key_Right:
            x += 1.0 / self.width()
          if e.key() == QtCore.Qt.Key_Up:
            y += 1.0 / self.height()
          if e.key() == QtCore.Qt.Key_Down:
            y -= 1.0 / self.height()
          self.warpGrid.points[selIdx] = (x,y)
          print(x,y)

 
    def mousePressEvent(self, e):
      self.oldx = e.x()
      self.oldy = e.y()
      newPos = self.screenPos()
      print(newPos)
      self.nearest = self.warpGrid.getNearest(newPos[0],newPos[1])
      if e.modifiers() == QtCore.Qt.ControlModifier:
        if self.nearest in self.warpGrid.selectedPoints:
          if len(self.warpGrid.selectedPoints) > 1: 
            self.warpGrid.selectedPoints.remove(self.nearest)
        else:
          self.warpGrid.selectedPoints.add(self.nearest)
      else:
        self.warpGrid.selectedPoints = set([self.nearest])
      self.isPressed = True


    def mouseReleaseEvent(self, e):
      self.isPressed = False
#      self.nearest = -1
#      if not (e.modifiers() == QtCore.Qt.ControlModifier):
#        self.warpGrid.selectedPoints = set()

    def screenPos(self):
      left, right, top, bottom = self.viewRect()
      width = right - left
      height = bottom - top
      return ((float(self.oldx) / self.width() - 0.5) * width,(1.0 - float(self.oldy) / self.height() - 0.5) * height)


