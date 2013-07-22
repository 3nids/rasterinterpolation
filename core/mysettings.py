"""
Plain Geometry Editor
QGIS plugin

Denis Rouzaud
denis.rouzaud@gmail.com
Jan. 2013
"""

from ..qgissettingmanager import *

pluginName = "rasterInterpolation"


class MySettings(SettingManager):
    def __init__(self):
        SettingManager.__init__(self, pluginName)
        self.addSetting("interpolationMethod", "string", "global", "bi-linear", {"comboMode": "text"})
        self.addSetting("processOnlyNull", "bool", "global", False)
        self.addSetting("processOnlySelected", "bool", "global", False)
        self.addSetting("additionValue", "double", "project", 0)
        self.addSetting("rasterLayer", "string", "project", "")
        self.addSetting("rasterBand", "integer", "project", 1)
        self.addSetting("vectorLayer", "string", "project", "")
        self.addSetting("destinationField", "string", "project", "")

