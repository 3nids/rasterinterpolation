"""
Plain Geometry Editor
QGIS plugin

Denis Rouzaud
denis.rouzaud@gmail.com
Jan. 2013
"""
from PyQt4.QtGui import QColor,QDialog

from qgistools.pluginsettings import *

pluginName = "landit"
landItSettings = [
		# global settings
		String( pluginName, "interpolationMethod", "global",  ""     , {"comboMode": "text"} ),
		Bool(   pluginName, "processOnlyNull"    , "global",  False  )                        ,
		# project settings
		Double( pluginName, "additionValue"      , "project", 0      )                        ,
		# fields and layers
		String( pluginName, "dtmLayer"           , "project", ""     )                        ,
		String( pluginName, "sourceLayer"        , "project", ""     )                        ,
		String( pluginName, "destinationField"   , "project", ""     )
		]

class MySettings(PluginSettings):
	def __init__(self):
		PluginSettings.__init__(self, landItSettings)
