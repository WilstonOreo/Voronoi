#! /usr/bin/env python

from __future__ import print_function

from PyQt4 import QtGui, QtCore, uic
from optparse import OptionParser
import qdarkstyle
import os, sys

class ProjectorItemWidget(QtGui.QWidget):
  def __init__(self):
    QtGui.QWidget.__init__(self)
    uic.loadUi('../app/ProjectorWidget.ui',self)
    s = "QGroupBox { border:2px solid #0000FF; border-radius: 9px; margin-top: 18px; }"
    s += "QGroupBox::title { color: #0000FF; "
    s += " background-color: qradialgradient(cx:0.5, cy:0.5, radius: 0.5,"
    s += " fx:0.5, fy:0.5, stop:0.2 black, stop:1 transparent) ; subcontrol-origin: margin;"
    s += "subcontrol-position: top center; padding-left: 10px;"
    s += "padding-right: 10px; }"
    self.setStyleSheet(s);

  def toggleSettings(self,b):
    return
  
  def toggleScreenSettings(self,b):
    return




class ProjectorList(QtGui.QScrollArea):
  def __init__(self):
    QtGui.QScrollArea.__init__(self)
    cssFile="qdarkstyle/style.qss"
    self.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
    
    self.items = QtGui.QGroupBox()
    
    layout = QtGui.QVBoxLayout()
    layout.setSizeConstraint(QtGui.QLayout.SetNoConstraint);
    self.setLayout(layout)
    self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    self.items.setLayout(layout)
    self.items.show()
    self.setWidget(self.items)

    self.setWidgetResizable(True)



  def add(self,proj1):
    self.items.layout().addWidget(proj1)

if __name__ == '__main__': 
  #parser = OptionParser()
  #(options, args) = parser.parse_args()

  app = QtGui.QApplication(['ProjectorListTest'])

  window = ProjectorList()

  window.add(ProjectorItemWidget())
  window.add(ProjectorItemWidget())
  window.add(ProjectorItemWidget())
  window.add(ProjectorItemWidget())

  window.show()

  sys.exit(app.exec_())
