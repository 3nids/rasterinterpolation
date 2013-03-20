"""
Plain Geometry Editor
QGIS plugin

Denis Rouzaud
denis.rouzaud@gmail.com
Jan. 2013
"""
from PyQt4.QtGui import QColor,QDialog

from qgistools.pluginsettings.pluginsettings import PluginSettings
from qgistools.pluginsettings.setting import Setting

pluginName = "landit"
landItSettings = [
		# global settings
		Setting(pluginName, "interpolationMethod", "global", "string" , ""     , {"comboMode": "text"} ),
		Setting(pluginName, "processOnlyNull"    , "global", "bool"   , False  )                        ,
		# project settings
		Setting(pluginName, "additionValue"      , "project", "double", 0      )                        ,
		# fields and layers
		Setting(pluginName, "dtmLayer"           , "project", "string", ""     )                        ,
		Setting(pluginName, "sourceLayer"        , "project", "string", ""     )                        ,
		Setting(pluginName, "destinationField"   , "project", "string", ""     )
		]

class MySettings(PluginSettings):
	def __init__(self):
		PluginSettings.__init__(self, landItSettings)
