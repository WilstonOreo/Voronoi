#! /usr/bin/env python
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

from PyQt4.QtOpenGL import *
import numpy
from OpenGL.GL import *
from OpenGL.GLU import *

# PyOpenGL 3.0.1 introduces this convenience module...
from OpenGL.GL.shaders import *


try:
    from PIL.Image import open as ImageOpen
except ImportError, err:
    from Image import open as ImageOpen

class Texture:
  def __init__(self,imageFilename):
    self.__texMode = GL_TEXTURE_2D
    self.imageID = self.loadImage(imageFilename)

  def setup(self): 
    #glTexEnvf( GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE );
    glEnable(self.__texMode)
    glActiveTexture(GL_TEXTURE0 + self.imageID)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)   
    glTexParameterf( self.__texMode, GL_TEXTURE_WRAP_S,GL_REPEAT);
    glTexParameterf( self.__texMode, GL_TEXTURE_WRAP_T,GL_REPEAT);
    glTexParameteri(self.__texMode, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(self.__texMode, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glBindTexture(self.__texMode, self.imageID)

  def loadImage( self, imageName):
    glEnable(self.__texMode)
    """Load an image file as a 2D texture using PIL"""
    im = ImageOpen(imageName)    
    img_data = numpy.array(im.getdata(), numpy.uint8)

    self.imageID = glGenTextures(1)
    print(self.imageID)
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glBindTexture(self.__texMode, self.imageID)
    glTexParameterf(self.__texMode, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(self.__texMode, GL_TEXTURE_WRAP_T, GL_REPEAT)
    #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(
        self.__texMode, 0, GL_RGB, im.size[0], im.size[1], 0,
        GL_RGB, GL_UNSIGNED_BYTE, img_data
    )
    return self.imageID
