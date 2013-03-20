"""
Intersect It QGIS plugin
Denis Rouzaud
denis.rouzaud@gmail.com
March. 2012
"""

def classFactory(iface):
    from landit import LandIt
    return LandIt(iface)
    




