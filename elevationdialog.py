"""
Landt It QGIS plugin
Denis Rouzaud
denis.rouzaud@gmail.com
March 2013
"""

# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

from ui.ui_landit import Ui_LandIt

from mysettings import MySettings, landItSettings
from qgistools.pluginsettings.pluginsettings import PluginSettings
from qgistools.gui.layerfieldcombomanager import LayerCombo, FieldCombo

class ElevationDialog(QDialog, Ui_LandIt, PluginSettings):
	def __init__(self, iface):
		QDialog.__init__(self)
		self.setupUi(self)
		
		setValuesOnDialogAccepted = False
		setValueOnWidgetUpdate    = True
		PluginSettings.__init__(self, landItSettings, setValuesOnDialogAccepted, setValueOnWidgetUpdate)
		
		self.dtmLayerCombo    = LayerCombo(iface, self.dtmLayer, lambda: self.value("dtmLayer"), False)
		self.sourceLayerCombo = LayerCombo(iface, self.sourceLayer, lambda: self.value("sourceLayer"), True)
		self.destinationFieldCombo = FieldCombo(self.destinationField, self.sourceLayerCombo, lambda: self.value("destinationField"))

	def showEvent(self, e):
		PluginSettings.showEvent(self, e)
		self.progressBar.hide()


