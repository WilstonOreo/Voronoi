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

from OpenGL.GL import *
from MyGeom import *

class Light:
  def __init__(self,index,position,diffuseColor = [1.0,1.0,1.0]):
    self.index = index
    self.position = position
    self.diffuseColor = diffuseColor
    self.setup()
    self.enable()

  def setup(self):
    glEnable( GL_LIGHTING )
    glEnable(GL_COLOR_MATERIAL)
    glLightModelfv(GL_LIGHT_MODEL_TWO_SIDE, [0.1,0.1,0.1] )
    glLightfv(self.index, GL_DIFFUSE, self.diffuseColor)
    glLightfv(self.index, GL_POSITION, self.position.coordinates)

  def enable(self):
    glEnable(self.index)

  def disable(self):
    glDisable(self.index)


''' A line segment with a draw function
'''
class Segment:
  def __init__(self,p0,p1):
    self.p0 = p0
    self.p1 = p1
  
  def draw(self,color):
    if len(color) == 3:
      glColor(color[0],color[1],color[2])
    else:
      glColor(color[0],color[1],color[2],color[3])
    
    glBegin(GL_LINE_STRIP)
    glVertex3fv(self.p0.get())
    glVertex3fv(self.p1.get())
    glEnd()


