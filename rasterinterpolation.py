"""
Landt It QGIS plugin
Denis Rouzaud
denis.rouzaud@gmail.com
March 2013
"""

from PyQt4.QtCore import QUrl
from PyQt4.QtGui import QAction, QIcon, QDesktopServices

import resources

from gui.elevationdialog import ElevationDialog


class RasterInterpolation ():
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        self.elevationDialog = ElevationDialog(self.iface)
          
        self.elevationAction = QAction(QIcon(":/plugins/rasterinterpolation/icons/rasterinterpolation.png"),
                                       "Raster Interpolation - calculate elevations", self.iface.mainWindow())
        self.elevationAction.triggered.connect(self.elevationDialog.show)
        self.iface.addToolBarIcon(self.elevationAction)
        self.iface.addPluginToMenu("&Raster Interpolation", self.elevationAction)
        # help
        self.helpAction = QAction("help", self.iface.mainWindow())
        self.helpAction.triggered.connect(self.help)
        self.iface.addPluginToMenu("&Raster Interpolation", self.helpAction)
          
    def help(self):
        QDesktopServices.openUrl(QUrl("https://github.com/3nids/rasterinterpolation"))

    def unload(self):
        self.iface.removePluginMenu("&Raster Interpolation", self.elevationAction)
        self.iface.removePluginMenu("&Raster Interpolation", self.helpAction)
        self.iface.removeToolBarIcon(self.elevationAction)
