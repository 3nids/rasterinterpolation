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

try:
	from scipy import interpolate
	from numpy import asscalar
	scipyAvailable = True
except:
	scipyAvailable = False

from ui.ui_landit import Ui_LandIt

from landitsettings import pluginName,landItSettings
from qgistools.pluginsettings import PluginSettings
from qgistools.gui import VectorLayerCombo, FieldCombo, RasterLayerCombo

class ElevationDialog(QDialog, Ui_LandIt, PluginSettings):
	def __init__(self, iface):
		QDialog.__init__(self)
		self.setupUi(self)
		self.setWindowFlags( Qt.WindowStaysOnTopHint )

		setValuesOnDialogAccepted = False
		setValueOnWidgetUpdate    = True
		PluginSettings.__init__(self, pluginName, landItSettings, setValuesOnDialogAccepted, setValueOnWidgetUpdate)

		self.dtmLayerCombo    = RasterLayerCombo(iface, self.dtmLayer   , lambda: self.value("dtmLayer"), {"groupLayers":True})
		self.vectorLayerCombo = VectorLayerCombo(iface, self.vectorLayer, lambda: self.value("vectorLayer"), {"groupLayers":True,"hasGeometry":True, "geomType": QGis.Point})
		self.destinationFieldCombo = FieldCombo(self.destinationField, self.vectorLayerCombo, lambda: self.value("destinationField"))

	def showEvent(self, e):
		PluginSettings.showEvent(self, e)
		self.progressBar.hide()
		self.stopButton.hide()
		self.messageLabel.clear()

	@pyqtSignature("on_stopButton_pressed()")
	def on_stopButton_pressed(self):
		self.continueProcess = False

	@pyqtSignature("on_doButton_clicked()")
	def on_doButton_clicked(self):
		self.messageLabel.clear()
		self.continueProcess = True
		dtmLayer = self.dtmLayerCombo.getLayer()
		vectorLayer = self.vectorLayerCombo.getLayer()
		fieldIdx = self.destinationFieldCombo.getFieldIndex()
		fieldName = self.destinationFieldCombo.getFieldName()
		interpol = self.interpolationMethod.currentIndex()
		additionValue = self.additionValue.value()

		if dtmLayer    is None:
			self.messageLabel.setText("specify DTM layer")
			return
		if vectorLayer is None:
			self.messageLabel.setText("specify source layer")
			return
		if not vectorLayer.isEditable():
			self.messageLabel.setText("source layer must editable")
			return
		if fieldName == "":
			self.messageLabel.setText("choose a field to save elevations")
			return
		if interpol == 2 and not scipyAvailable:
			self.messageLabel.setText("scipy must be installed for cubic interpolation")
			return

		self.progressBar.setMinimum(0)
		self.progressBar.setMaximum(1)
		self.progressBar.setValue(0)
		self.progressBar.show()
		self.stopButton.show()
		k = 0
		f = QgsFeature()
		if self.processOnlySelected.isChecked():
			self.progressBar.setMaximum(vectorLayer.selectedFeatureCount())
			ids = vectorLayer.selectedFeaturesIds()
			for id in ids:
				k+=1
				self.progressBar.setValue(k)
				vectorLayer.getFeatures( QgsFeatureRequest( id ) ).nextFeature( f )
				if self.processOnlyNull.isChecked() and not f.attribute(fieldName).isNull():
					continue
				self.calculateElevation( dtmLayer, vectorLayer, f, fieldIdx, interpol, additionValue)
				QCoreApplication.processEvents()
				if not self.continueProcess: break
		else:
			self.progressBar.setMaximum(vectorLayer.dataProvider().featureCount())
			iter = vectorLayer.getFeatures( QgsFeatureRequest() )
			while iter.nextFeature( f ):
				k+=1
				self.progressBar.setValue(k)
				if self.processOnlyNull.isChecked() and not f.attribute(fieldName).isNull():
					continue
				self.calculateElevation( dtmLayer, vectorLayer, f, fieldIdx, interpol, additionValue)
				QCoreApplication.processEvents()
				if not self.continueProcess: break
		self.progressBar.hide()
		self.stopButton.hide()


	def calculateElevation(self, dtmLayer, vectorLayer, f, fieldIdx, interpolMethod, additionValue):
		prov = dtmLayer.dataProvider()
		thePoint = f.geometry().asPoint()
		alt = None
		if interpolMethod == 0: # nearest neighbor
			ident = prov.identify( thePoint, QgsRasterDataProvider.IdentifyFormatValue )
			if ident is not None:# and ident.has_key(choosenBand+1):
				alt = ident[1].toDouble()[0]
		elif interpolMethod == 1: # bilinear interpolation
			# see the implementation of raster data provider, identify method
			# https://github.com/qgis/Quantum-GIS/blob/master/src/core/raster/qgsrasterdataprovider.cpp#L268
			x = thePoint.x()
			y = thePoint.y()
			myExtent = prov.extent()
			theWidth  = prov.xSize()
			theHeight = prov.ySize()
			xres = myExtent.width()  / theWidth
			yres = myExtent.height() / theHeight
			col = round(( x - myExtent.xMinimum() ) / xres )
			row = round(( myExtent.yMaximum() - y ) / yres )
			xMin = myExtent.xMinimum() + (col-1) * xres
			xMax = xMin + 2*xres
			yMax = myExtent.yMaximum() - (row-1) * yres
			yMin = yMax - 2*yres
			pixelExtent = QgsRectangle( xMin, yMin, xMax, yMax )
			myBlock = prov.block( 1, pixelExtent, 2, 2 )
			# http://en.wikipedia.org/wiki/Bilinear_interpolation#Algorithm
			v12 = myBlock.value( 0, 0 )
			v22 = myBlock.value( 0, 1 )
			v11 = myBlock.value( 1, 0 )
			v21 = myBlock.value( 1, 1 )
			x1 = xMin+xres/2
			x2 = xMax-xres/2
			y1 = yMin+yres/2
			y2 = yMax-yres/2
			alt = 	( v11*(x2-x )*(y2-y )
					+ v21*(x -x1)*(y2-y )
					+ v12*(x2-x )*(y -y1)
					+ v22*(x -x1)*(y -y1)
					) / ( (x2-x1)*(y2-y1) )
		elif interpolMethod == 2: # bicubic interpolation
			# see the implementation of raster data provider, identify method
			# https://github.com/qgis/Quantum-GIS/blob/master/src/core/raster/qgsrasterdataprovider.cpp#L268
			x = thePoint.x()
			y = thePoint.y()
			myExtent = prov.extent()
			theWidth  = prov.xSize()
			theHeight = prov.ySize()
			xres = myExtent.width()  / theWidth
			yres = myExtent.height() / theHeight
			col = round(( x - myExtent.xMinimum() ) / xres )
			row = round(( myExtent.yMaximum() - y ) / yres )
			xMin = myExtent.xMinimum() + (col-2) * xres
			xMax = xMin + 4*xres
			yMax = myExtent.yMaximum() - (row-2) * yres
			yMin = yMax - 4*yres
			pixelExtent = QgsRectangle( xMin, yMin, xMax, yMax )
			myBlock = prov.block( 1, pixelExtent, 4, 4 )
			# http://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.interp2d.html
			vx = [xMin+.5*xres , xMin+1.5*xres , xMin+2.5*xres , xMin+3.5*xres]
			vy = [yMin+.5*yres , yMin+1.5*yres , yMin+2.5*yres , yMin+3.5*yres]
			vz = [	[myBlock.value(3,0),myBlock.value(3,1),myBlock.value(3,2),myBlock.value(3,3)],
					[myBlock.value(2,0),myBlock.value(2,1),myBlock.value(2,2),myBlock.value(2,3)],
					[myBlock.value(1,0),myBlock.value(1,1),myBlock.value(1,2),myBlock.value(1,3)],
					[myBlock.value(0,0),myBlock.value(0,1),myBlock.value(0,2),myBlock.value(0,3)] ]
			fz = interpolate.interp2d(vx,vy,vz,kind='cubic')
			alt = asscalar( fz(x,y)[0] )

		if alt is not None and prov.isNoDataValue( 1, alt ):
			alt = None
		if alt is not None:
			alt += additionValue
		res = vectorLayer.changeAttributeValue( f.id(), fieldIdx, alt )
		print alt, res

