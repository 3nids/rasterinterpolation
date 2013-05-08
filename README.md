## About

**Raster Interpolation** is a [QGIS](http://www.qgis.org) plugin to interpolates values on a raster layer.

The plugin will loop through a layer of points, interpolate the value at their position on the raster and save this value in the chosen field.

It can be used to calculate elevation from a DTM.

## Features

* Interpolation: nearest neighbot, linear or bicubic* interpolation
* Process can be limited to a selection or to yet undefined values
* Choose band to process in the raster

*[scipy](http://www.scipy.org/) is required

## Screenshot

!(https//raw.github.com/3nids/rasterinterpolation/tree/master/doc/screenshot.png)
