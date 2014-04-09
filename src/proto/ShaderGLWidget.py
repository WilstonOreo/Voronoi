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

from PyQt4.QtOpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math
import time
import os

try:
    from PIL.Image import open as ImageOpen
except ImportError, err:
    from Image import open as ImageOpen

from Base import *
from Texture import Texture
from Shader import Shader

TEXTURE_PATH = "./images"


class ShaderGLWidget(QGLWidget):
    def __init__(self, parent):
      QGLWidget.__init__(self, parent)
      self.shader = None
      self.setMouseTracking(True)
      self.isPressed = False
      self.oldx = self.oldy = 0
      self.textures = []
      self.vertexFile = ""
      self.fragmentFile = ""
      self.uniformFile = ""
      self.textureFile = ""
      self.startTime = float(time.time())

    def loadUniformFile(self):
      if not self.uniformFile: return
      f = open(self.uniformFile,'r')
      self.uniforms = []
      for line in f:
        self.uniforms.append(line.strip().split())
      self.lastUniformEdit = os.stat(self.uniformFile).st_mtime
    
    def loadTextureFile(self):
      if not self.textureFile: return
      f = open(self.textureFile,'r')
      self.textures = []
      
      for line in f:
        l = line.strip()
        if not l: continue
        self.textures.append(Texture(l))

    def paintGL(self): 
      if self.shader is None: return
      if os.stat(self.fragmentFile).st_mtime != self.lastEdit:
        self.loadShader()
      
      if os.stat(self.uniformFile).st_mtime != self.lastUniformEdit:
        self.loadUniformFile()
            
      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
      glDisable( GL_DEPTH_TEST )
      glDisable( GL_CULL_FACE ) 

      glDisable(GL_TEXTURE_2D)
      glLoadIdentity()
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()
      gluOrtho2D(0,1,0,1)

      glMatrixMode(GL_MODELVIEW)
      glLoadIdentity()

 
      self.shader.use()
      for texture in self.textures:
        texture.setup()


      #self.canvasModel.shaderSettings(shader)
      for uniform in self.uniforms:
        vecType = uniform[0]
        key = uniform[1]
        
        valuesStr = uniform[2:]
        values = []

        from math import sin
        from math import cos

        t = float(time.time()) - self.startTime
        x = 20.0*(self.oldx / float(self.width()) - 0.5)
        y = 20.0*(self.oldy / float(self.height()) - 0.5)
        resx = self.width()
        resy = self.height()
        
        for v in valuesStr:
          val = eval(v)
          values.append(val)
        self.shader.setUniform(vecType,key,[values])
      
     # self.shader.set(
     #     plane_height = ("1f",[4.0]),
     #     checker_offset = ("2f",[(4.0,4.0)]),
     #     checker_scale = ("2f",[(1.0,1.0)]), 
     #     sphere_radius = ("1f",[1.0]),
     #     sphere_center = ("3f",[(0.0,1.0,2.0)]) 
     #     )
 
      glBegin(GL_QUADS)
      glColor4f(1.0,1.0,1.0,1.0)
      glTexCoord2f(0.0, 0.0); glVertex2f(0.0,0.0)
      glTexCoord2f(1.0, 0.0); glVertex2f(1.0,0.0) 
      glTexCoord2f(1.0, 1.0); glVertex2f(1.0,1.0)
      glTexCoord2f(0.0, 1.0); glVertex2f(0.0,1.0)
      glEnd()

    
      self.shader.unuse()
      self.update()
      #glFlush()

    def resizeGL(self, widthInPixels, heightInPixels):
      glViewport(0, 0, widthInPixels, heightInPixels)

    def initializeGL(self):
      glClearColor(0.0, 0.0, 0.0, 1.0)
      glClearDepth(1.0)
      self.loadShader()
      self.loadUniformFile()
      self.loadTextureFile()
    
    def loadShader(self):
      if self.vertexFile and self.fragmentFile:
        self.shader = Shader(self.vertexFile,self.fragmentFile)    
        self.lastEdit = os.stat(self.fragmentFile).st_mtime

    def mouseMoveEvent(self, mouseEvent):
        self.oldx = mouseEvent.x()
        self.oldy = mouseEvent.y()
 
    def mousePressEvent(self, e):
      self.isPressed = True

    def mouseReleaseEvent(self, e):
      self.isPressed = False

