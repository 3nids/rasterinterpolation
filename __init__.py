"""
Intersect It QGIS plugin
Denis Rouzaud
denis.rouzaud@gmail.com
March. 2012
"""

def classFactory(iface):
    from rasterinterpolation import RasterInterpolation
    return RasterInterpolation(iface)
    




