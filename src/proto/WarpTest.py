#! /usr/bin/env python

from __future__ import print_function

from PyQt4 import QtGui, QtCore, uic
from OpenGL.GLUT import *

import os, sys
import WarpGLWidget

if __name__ == '__main__': 
  app = QtGui.QApplication(['WarpTest'])
  glutInit(sys.argv)
  

  window = WarpGLWidget.WarpGLWidget(None)
  window.show()
  sys.exit(app.exec_())

