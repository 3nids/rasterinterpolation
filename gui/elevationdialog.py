"""
Landt It QGIS plugin
Denis Rouzaud
denis.rouzaud@gmail.com
March 2013
"""

from PyQt4.QtCore import Qt, pyqtSignature, QCoreApplication
from PyQt4.QtGui import QDialog
from qgis.core import QGis, QgsFeature, QgsFeatureRequest

from qgiscombomanager import VectorLayerCombo, RasterLayerCombo, FieldCombo
from qgissettingmanager import SettingDialog

from ..core.mysettings import MySettings
from ..core.rasterinterpolator import RasterInterpolator, ScipyAvailable

from ..ui.ui_elevationdialog import Ui_ElevationDialog


class ElevationDialog(QDialog, Ui_ElevationDialog, SettingDialog):
    def __init__(self, iface):
        QDialog.__init__(self)
        self.setupUi(self)
        self.settings = MySettings()
        setValuesOnDialogAccepted = False
        setValueOnWidgetUpdate = True
        SettingDialog.__init__(self, self.settings, setValuesOnDialogAccepted, setValueOnWidgetUpdate)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        legendInterface = iface.legendInterface()

        self.rasterLayerCombo = RasterLayerCombo(legendInterface, self.rasterLayer,
                                              lambda: self.settings.value("rasterLayer"), {"groupLayers": True})
        self.vectorLayerCombo = VectorLayerCombo(legendInterface, self.vectorLayer,
                                                 lambda: self.settings.value("vectorLayer"),
                                                 {"groupLayers": True, "hasGeometry": True, "geomType": QGis.Point})
        self.destinationFieldCombo = FieldCombo(self.destinationField, self.vectorLayerCombo,
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
        rasterLayer = self.rasterLayerCombo.getLayer()
        band = self.rasterBand.getFieldIndex()+1
        vectorLayer = self.vectorLayerCombo.getLayer()
        fieldIdx = self.destinationFieldCombo.getFieldIndex()
        fieldName = self.destinationFieldCombo.getFieldName()
        interpol = self.interpolationMethod.currentIndex()
        additionValue = self.additionValue.value()

        if rasterLayer is None:
            self.messageLabel.setText("specify raster layer")
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
        if interpol == 2 and not ScipyAvailable:
            self.messageLabel.setText("scipy must be installed for cubic interpolation")
            return

        rasterInterpolator = RasterInterpolator(rasterLayer, vectorLayer, interpol, band)
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
        alt = interpolator.elevation(thePoint)
        if alt is not None:
            alt += additionValue
        vectorLayer.changeAttributeValue(f.id(), fieldIdx, alt)