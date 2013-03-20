# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_landit.ui'
#
# Created: Wed Mar 20 14:58:53 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_LandIt(object):
    def setupUi(self, LandIt):
        LandIt.setObjectName(_fromUtf8("LandIt"))
        LandIt.resize(384, 205)
        self.gridLayout = QtGui.QGridLayout(LandIt)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.checkBox = QtGui.QCheckBox(LandIt)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.gridLayout.addWidget(self.checkBox, 6, 0, 1, 3)
        self.widget = QtGui.QWidget(LandIt)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.widget)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.destinationField = QtGui.QComboBox(self.widget)
        self.destinationField.setObjectName(_fromUtf8("destinationField"))
        self.gridLayout_2.addWidget(self.destinationField, 1, 3, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 4, 1, 1)
        self.gridLayout.addWidget(self.widget, 4, 0, 1, 3)
        self.pushButton = QtGui.QPushButton(LandIt)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 7, 2, 1, 1)
        self.widget_4 = QtGui.QWidget(LandIt)
        self.widget_4.setObjectName(_fromUtf8("widget_4"))
        self.gridLayout_5 = QtGui.QGridLayout(self.widget_4)
        self.gridLayout_5.setMargin(0)
        self.gridLayout_5.setMargin(0)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.label_3 = QtGui.QLabel(self.widget_4)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_5.addWidget(self.label_3, 0, 0, 1, 1)
        self.interpolationMathod = QtGui.QComboBox(self.widget_4)
        self.interpolationMathod.setObjectName(_fromUtf8("interpolationMathod"))
        self.interpolationMathod.addItem(_fromUtf8(""))
        self.interpolationMathod.addItem(_fromUtf8(""))
        self.interpolationMathod.addItem(_fromUtf8(""))
        self.gridLayout_5.addWidget(self.interpolationMathod, 0, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem1, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.widget_4, 5, 0, 1, 3)
        self.progressBar = QtGui.QProgressBar(LandIt)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 7, 0, 1, 2)
        self.widget_3 = QtGui.QWidget(LandIt)
        self.widget_3.setObjectName(_fromUtf8("widget_3"))
        self.gridLayout_4 = QtGui.QGridLayout(self.widget_3)
        self.gridLayout_4.setMargin(0)
        self.gridLayout_4.setMargin(0)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.label = QtGui.QLabel(self.widget_3)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_4.addWidget(self.label, 1, 0, 1, 1)
        self.sourceLayercomboBox = QtGui.QComboBox(self.widget_3)
        self.sourceLayercomboBox.setObjectName(_fromUtf8("sourceLayercomboBox"))
        self.gridLayout_4.addWidget(self.sourceLayercomboBox, 1, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem2, 1, 2, 1, 1)
        self.gridLayout.addWidget(self.widget_3, 1, 0, 1, 3)
        self.widget_2 = QtGui.QWidget(LandIt)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.widget_2)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_4 = QtGui.QLabel(self.widget_2)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_3.addWidget(self.label_4, 0, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem3, 0, 2, 1, 1)
        self.dtmLayerComboBox = QtGui.QComboBox(self.widget_2)
        self.dtmLayerComboBox.setObjectName(_fromUtf8("dtmLayerComboBox"))
        self.gridLayout_3.addWidget(self.dtmLayerComboBox, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.widget_2, 0, 0, 1, 3)

        self.retranslateUi(LandIt)
        QtCore.QMetaObject.connectSlotsByName(LandIt)

    def retranslateUi(self, LandIt):
        LandIt.setWindowTitle(QtGui.QApplication.translate("LandIt", "LandIt", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("LandIt", "Only process point where destination field is NULL", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("LandIt", "Destination field", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("LandIt", "go", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("LandIt", "Interpolation method", None, QtGui.QApplication.UnicodeUTF8))
        self.interpolationMathod.setItemText(0, QtGui.QApplication.translate("LandIt", "nearest neighbor", None, QtGui.QApplication.UnicodeUTF8))
        self.interpolationMathod.setItemText(1, QtGui.QApplication.translate("LandIt", "linear interpolation", None, QtGui.QApplication.UnicodeUTF8))
        self.interpolationMathod.setItemText(2, QtGui.QApplication.translate("LandIt", "cubic interpolation", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("LandIt", "Points from layer", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("LandIt", "DTM", None, QtGui.QApplication.UnicodeUTF8))

