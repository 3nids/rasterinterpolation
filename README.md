## About

**Raster Interpolation** is a [QGIS](http://www.qgis.org) plugin to interpolates values on raster layers.

It browses a vector layer of points, interpolates at their position the value of a raster layer and save the value in a chosen field of the vector layer.

Interpolation can be nearest, linear or bi-cubic. Simple filter on the vector layer may be applied (browse only currently NULL values and/or only selected features).

It can be used to calculate elevation from a DTM.

## Features

* Interpolation: nearest neighbot, linear or bicubic* interpolation
* Process can be limited to a selection or to yet undefined values
* Choose band to process in the raster

*[scipy](http://www.scipy.org/) is required

## Screenshot

![screenshot](https://raw.github.com/3nids/rasterinterpolation/master/doc/screenshot.png)
