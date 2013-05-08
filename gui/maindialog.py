"""
Landt It QGIS plugin
Denis Rouzaud
denis.rouzaud@gmail.com
March 2013
"""

from PyQt4.QtCore import Qt, pyqtSignature, QCoreApplication
from PyQt4.QtGui import QDialog
from qgis.core import QGis, QgsFeature, QgsFeatureRequest

from ..qgiscombomanager import VectorLayerCombo, RasterLayerCombo, FieldCombo, BandCombo
from ..qgissettingmanager import SettingDialog

from ..core.mysettings import MySettings
from ..core.rasterinterpolator import RasterInterpolator, ScipyAvailable

from ..ui.ui_maindialog import Ui_MainDialog


class MainDialog(QDialog, Ui_MainDialog, SettingDialog):
    def __init__(self, legendInterface):
        QDialog.__init__(self)
        self.setupUi(self)
        self.settings = MySettings()
        setValuesOnDialogAccepted = False
        setValueOnWidgetUpdate = True
        SettingDialog.__init__(self, self.settings, setValuesOnDialogAccepted, setValueOnWidgetUpdate)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.rasterLayerManager = RasterLayerCombo(self.rasterLayer, lambda: self.settings.value("rasterLayer"),
                                                   {"groupLayers": True, "legendInterface": legendInterface})
        self.rasterBandManager = BandCombo(self.rasterBand, self.rasterLayerManager,
                                           lambda: self.settings.value("rasterBand"))
        self.vectorLayerManager = VectorLayerCombo(self.vectorLayer, lambda: self.settings.value("vectorLayer"),
                                                   {"groupLayers": True, "legendInterface": legendInterface,
                                                    "hasGeometry": True, "geomType": QGis.Point})
        self.destinationFieldManager = FieldCombo(self.destinationField, self.vectorLayerManager,
                                                  lambda: self.settings.value("destinationField"))

    def showEvent(self, e):
        SettingDialog.showEvent(self, e)
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
        rasterLayer = self.rasterLayerManager.getLayer()
        band = self.rasterBandManager.getBand()
        vectorLayer = self.vectorLayerManager.getLayer()
        fieldIdx = self.destinationFieldManager.getFieldIndex()
        fieldName = self.destinationFieldManager.getFieldName()
        interpol = self.interpolationMethod.currentIndex()
        additionValue = self.additionValue.value()

        if rasterLayer is None:
            self.messageLabel.setText("specify raster layer")
            return
        if vectorLayer is None:
            self.messageLabel.setText("specify source layer")
            return
        if band == 0:
            self.messageLabel.setText("specify a band fro the raster layer")
            return
        if not vectorLayer.isEditable():
            self.messageLabel.setText("source layer must editable")
            return
        if fieldName == "":
            self.messageLabel.setText("choose a field to save elevations")
            return
        if interpol == 2 and not ScipyAvailable:
            self.messageLabel.setText("scipy must be installed for cubic interpolation")
            return

        rasterInterpolator = RasterInterpolator(rasterLayer, interpol, band)
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
            for fid in ids:
                k += 1
                self.progressBar.setValue(k)
                vectorLayer.getFeatures(QgsFeatureRequest(fid)).nextFeature(f)
                if self.processOnlyNull.isChecked() and not f.attribute(fieldName).isNull():
                    continue
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
                if self.processOnlyNull.isChecked() and not f.attribute(fieldName).isNull():
                    continue
                self.writeInterpolation(f, fieldIdx, rasterInterpolator, vectorLayer, additionValue)
                QCoreApplication.processEvents()
                if not self.continueProcess:
                    break
        self.progressBar.hide()
        self.stopButton.hide()

    def writeInterpolation(self, f, fieldIdx, interpolator, vectorLayer, additionValue):
        thePoint = f.geometry().asPoint()
        alt = interpolator.interpolate(thePoint)
        if alt is not None:
            alt += additionValue
        vectorLayer.changeAttributeValue(f.id(), fieldIdx, alt)