"""
Landt It QGIS plugin
Denis Rouzaud
denis.rouzaud@gmail.com
March 2013
"""

from PyQt4.QtCore import Qt, pyqtSlot, QCoreApplication
from PyQt4.QtGui import QDialog
from qgis.core import QGis, QgsFeature, QgsFeatureRequest, NULL
from qgis.gui import QgsMessageBar

from ..qgiscombomanager import VectorLayerCombo, RasterLayerCombo, FieldCombo, BandCombo
from ..qgissettingmanager import SettingDialog

from ..core.mysettings import MySettings
from ..core.rasterinterpolator import RasterInterpolator, ScipyAvailable

from ..ui.ui_maindialog import Ui_MainDialog


class MainDialog(QDialog, Ui_MainDialog, SettingDialog):
    def __init__(self, iface):
        self.iface = iface
        QDialog.__init__(self)
        self.setupUi(self)
        self.settings = MySettings()
        setValuesOnDialogAccepted = False
        setValueOnWidgetUpdate = True
        SettingDialog.__init__(self, self.settings, setValuesOnDialogAccepted, setValueOnWidgetUpdate)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.rasterLayerManager = RasterLayerCombo(self.rasterLayer, lambda: self.settings.value("rasterLayer"))
        self.rasterBandManager = BandCombo(self.rasterBand, self.rasterLayerManager,
                                           lambda: self.settings.value("rasterBand"))
        self.vectorLayerManager = VectorLayerCombo(self.vectorLayer, lambda: self.settings.value("vectorLayer"),
                                                   {"hasGeometry": True, "geomType": QGis.Point})
        self.destinationFieldManager = FieldCombo(self.destinationField, self.vectorLayerManager,
                                                  lambda: self.settings.value("destinationField"))

    def showEvent(self, e):
        SettingDialog.showEvent(self, e)
        self.progressBar.hide()
        self.stopButton.hide()

    @pyqtSlot(name="on_stopButton_pressed")
    def on_stopButton_pressed(self):
        self.continueProcess = False

    @pyqtSlot(name="on_doButton_clicked")
    def on_doButton_clicked(self):
        self.continueProcess = True
        rasterLayer = self.rasterLayerManager.getLayer()
        band = self.rasterBandManager.getBand()
        vectorLayer = self.vectorLayerManager.getLayer()
        fieldIdx = self.destinationFieldManager.getFieldIndex()
        fieldName = self.destinationFieldManager.getFieldName()
        interpol = self.interpolationMethod.currentIndex()
        additionValue = self.additionValue.value()

        if rasterLayer is None:
            self.iface.messageBar().pushMessage("Raster Interpolation", "You must choose a raster layer.",
                                                QgsMessageBar.WARNING, 3)
            return
        if vectorLayer is None:
            self.iface.messageBar().pushMessage("Raster Interpolation", "You must choose a destination layer.",
                                                QgsMessageBar.WARNING, 3)
            return
        if band == 0:
            self.iface.messageBar().pushMessage("Raster Interpolation", "You must choose a band for the raster layer.",
                                                QgsMessageBar.WARNING, 3)
            return
        if not vectorLayer.isEditable():
            self.iface.messageBar().pushMessage("Raster Interpolation", "The destination layer must be editable.",
                                                QgsMessageBar.WARNING, 3)
            return
        if fieldName == "":
            self.iface.messageBar().pushMessage("Raster Interpolation", "You must choose a field to write values.",
                                                QgsMessageBar.WARNING, 3)
            return
        if interpol == 2 and not ScipyAvailable:
            self.iface.messageBar().pushMessage("Raster Interpolation",
                                                "Scipy should be installed for cubic interpolation.",
                                                QgsMessageBar.WARNING, 3)
            return

        rasterInterpolator = RasterInterpolator(rasterLayer, interpol, band)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(1)
        self.progressBar.setValue(0)
        self.progressBar.show()
        self.stopButton.show()
        k = 0
        c = 0
        f = QgsFeature()
        if self.processOnlySelected.isChecked():
            self.progressBar.setMaximum(vectorLayer.selectedFeatureCount())
            ids = vectorLayer.selectedFeaturesIds()
            for fid in ids:
                k += 1
                self.progressBar.setValue(k)
                vectorLayer.getFeatures(QgsFeatureRequest(fid)).nextFeature(f)
                if self.processOnlyNull.isChecked() and not f[fieldName] == NULL:
                    continue
                c += 1
                self.writeInterpolation(f, fieldIdx, rasterInterpolator, vectorLayer, additionValue)
                QCoreApplication.processEvents()
                if not self.continueProcess:
                    break
        else:
            self.progressBar.setMaximum(vectorLayer.dataProvider().featureCount())
            iterator = vectorLayer.getFeatures(QgsFeatureRequest())
            while iterator.nextFeature(f):
                k += 1
                self.progressBar.setValue(k)
                if self.processOnlyNull.isChecked() and not f[fieldName] == NULL:
                    continue
                c += 1
                self.writeInterpolation(f, fieldIdx, rasterInterpolator, vectorLayer, additionValue)
                QCoreApplication.processEvents()
                if not self.continueProcess:
                    break
        self.progressBar.hide()
        self.stopButton.hide()
        self.iface.messageBar().pushMessage("Raster Interpolation",
                                            "%u values have been updated in layer %s over %u points" %
                                            (c, vectorLayer.name(), k),
                                            QgsMessageBar.INFO, 3)

    def writeInterpolation(self, f, fieldIdx, interpolator, vectorLayer, additionValue):
        thePoint = f.geometry().asPoint()
        value = interpolator.interpolate(thePoint)
        if value is not None:
            value += additionValue
        vectorLayer.changeAttributeValue(f.id(), fieldIdx, value)
