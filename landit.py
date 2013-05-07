"""
Landt It QGIS plugin
Denis Rouzaud
denis.rouzaud@gmail.com
March 2013
"""

# Import the PyQt and QGIS libraries
from PyQt4.QtCore import QObject, QUrl
from PyQt4.QtGui import QAction, QIcon, QDesktopServices

import resources

from elevationdialog import ElevationDialog


class LandIt ():
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        self.elevationDialog = ElevationDialog(self.iface)
          
        self.elevationAction = QAction(QIcon(":/plugins/landit/icons/landit.png"), "Land It - calculate elevations",
                                       self.iface.mainWindow())
        self.elevationAction.triggered.connect(self.elevationDialog.show)
        self.iface.addToolBarIcon(self.elevationAction)
        self.iface.addPluginToMenu("&Land It", self.elevationAction)
        # help
        self.helpAction = QAction("help", self.iface.mainWindow())
        self.helpAction.triggered.connect(self.help)
        self.iface.addPluginToMenu("&Land It", self.helpAction)
          
    def help(self):
        QDesktopServices.openUrl(QUrl("https://github.com/3nids/landit/wiki"))

    def unload(self):
        self.iface.removePluginMenu("&Land It",self.elevationAction)
        self.iface.removePluginMenu("&Land It",self.helpAction)
        self.iface.removeToolBarIcon(self.elevationAction)
