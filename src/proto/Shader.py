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

import OpenGL 
OpenGL.ERROR_ON_COPY = True 
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
 
# PyOpenGL 3.0.1 introduces this convenience module...
from OpenGL.GL.shaders import *

def getShader(filename,excludedHeaders):
  PREFIX = "#include"
  def getIncludeFilename(line):
    s = line[len(PREFIX):] 
    s = s.lstrip('"< \t\n')
    s = s.rstrip('"> \t\n')

    candidates = [
        os.path.join(os.path.dirname(filename),s),s] 
    for path in sys.path:
      candidates.append(os.path.join(os.path.dirname(path),s))
   # print(candidates)
    for candidate in candidates:
      if os.path.exists(candidate):
        return candidate

  f = open(filename,'r')
  shaderStr = ""
  lineNr = 0
  for line in f:
    lineNr += 1
    if line.startswith(PREFIX):
      filename = getIncludeFilename(line.strip())
      if filename is not None:  
        shaderStr += "/" * 10 + " " + filename + " " + "/" * 10 + "\n" 
        filename = getIncludeFilename(line.strip())
        if not filename in excludedHeaders:
          shaderStr += getShader(filename,excludedHeaders)
          excludedHeaders.add(filename)
      else:
        print("Include file %s (line %d) not found, aborting!" % (line.strip(),lineNr))
        return
    else:
      shaderStr += line
  return shaderStr


class Shader:
  def __init__(self,vertFilename,fragFilename):
    def catchException(err):
      errString = err[0]

      ## NVIDIA
      #posToken = errString.split(":")[1]
      #lineNumber = int(posToken.strip().lstrip("0123456789").lstrip("(").rstrip(")"))
       
      ## ATI
      posToken = errString.split(":")[2]
      lineNumber = int(posToken.split('(')[0])
      
      source = err[1][0].split('\n')
      lineIdx = 1
      lines = 20
      print(err[0])
      for line in source:
        if (lineIdx - lines <= lineNumber) and (lineIdx + lines > lineNumber):
          suffix = "<<<<<<<<" if lineIdx == lineNumber else ""
          prefix = ">>>>>>>>" if lineIdx == lineNumber else ""
          print(str(lineIdx)+"\t"+prefix+"\t"+line+"\t"+suffix)
        lineIdx += 1
#      print(err[1][0])

    vertexShaderSource = getShader(vertFilename,set(vertFilename))
    fragmentShaderSource = getShader(fragFilename,set(fragFilename))

    vertexShader = compileShader(vertexShaderSource,GL_VERTEX_SHADER)
    try:
      fragmentShader = compileShader(fragmentShaderSource,GL_FRAGMENT_SHADER)
    except RuntimeError as err:
      catchException(err)

    self.program = compileProgram(vertexShader,fragmentShader)
  
  def set(self,**kwargs):
    for key in kwargs:
      self.setUniform(kwargs[key][0],key,kwargs[key][1])
  
  def setArgs(self,prefix,argList):
    for arg in argList:
      self.setUniform("1f",prefix+"_"+arg[0],[arg[1]])

  def setUniform(self,vecType,key,value):
    #loc = glGetUniformLocation(self.program,key)
    loc = self.__getUniform(key)
    if loc is not None: 
      #glUniform1i(loc,value)
      getattr(OpenGL.GL.shaders,'glUniform'+vecType+'v')(loc,len(value),value)
    
  def __getUniform(self,key):
    if not self.program: return
    loc = glGetUniformLocation(self.program,key)
    if not loc in (None,-1): 
      return loc

  """ Dictionary has the form:
      { varName : ("1f",[10]) }
      { varName : ("3f",[(1,2,3),(3,4,5)]) }
  """
  def use(self,**kwargs):
    for key in kwargs:
      self.__setUniform(key,kwargs[key][0],kwargs[key][1])
    glUseProgram(self.program)

  def unuse(self):
  	#Start using our program
	  glUseProgram(0) #self.program)

