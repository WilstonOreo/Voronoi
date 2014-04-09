#! /usr/bin/env python

from __future__ import print_function

from PyQt4 import QtGui, QtCore, uic
from OpenGL.GLUT import *
from optparse import OptionParser

import os, sys
import Shader

class ShaderTest(QtGui.QMainWindow):
  def __init__(self,vertexFile,fragmentFile,uniforms,textures):
    QtGui.QMainWindow.__init__(self)
    uic.loadUi('ShaderTest.ui', self)  
    self.show()

    self.glWidget.vertexFile = vertexFile
    self.glWidget.fragmentFile = fragmentFile
#    if uniforms is not None:
    if uniforms:
      self.glWidget.uniformFile = uniforms
    if textures:
      self.glWidget.textureFile = textures
    self.glWidget.initializeGL()



if __name__ == '__main__': 
  parser = OptionParser()
  parser.add_option("-s","--shader",action="store",type="string",dest="shader") 
  parser.add_option("-f","--fragment", action="store", type="string", dest="fragment")
  parser.add_option("-v","--vertex", action="store", type="string",dest="vertex")
  parser.add_option("-c","--compile", action="store", type="string",dest="compile")
  parser.add_option("-u","--uniforms", action="store", 
      type="string",dest="uniforms",default="")
  parser.add_option("-t","--textures", action="store", 
      type="string",dest="textures",default="")
  
  (options, args) = parser.parse_args()

  if options.compile is not None:
    print(Shader.getShader(options.compile,set(options.compile)))
    exit()


  app = QtGui.QApplication(['ShaderTest'])
  glutInit(sys.argv)
  
  vertex = options.vertex
  fragment = options.fragment 
  
  if options.shader is not None: 
    vertex = options.shader+".vert"
    fragment = options.shader+".frag"

  window = ShaderTest(vertex,fragment,options.uniforms,options.textures)
  window.setGeometry(0,0,512,512)
  window.show()
  sys.exit(app.exec_())

