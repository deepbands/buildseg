# buildseg
[![Python 3.8](https://img.shields.io/badge/python-3.8-red.svg)](https://www.python.org/downloads/release/python-360/) [![PaddlePaddle 2.2](https://img.shields.io/badge/paddlepaddle-2.2-green.svg)](https://www.python.org/downloads/release/python-360/) [![QGIS 3.16.11](https://img.shields.io/badge/qgis-3.16.11-blue.svg)](https://www.python.org/downloads/release/python-360/)

buildseg is a building extraction plugin of QGIS based on PaddlePaddle.

![gasd](https://user-images.githubusercontent.com/71769312/144436933-f22c6a14-706f-406b-ad04-c0e784ed317b.gif)

## TODO

- [x] Extract building on 512x512 remote sensing images.
- [x] Extract building on big remote sensing images through sliding frame and splicing.
- [ ] Replace the model and parameters (large-scale data).
- [ ] Convert to static weight.
- [ ] Hole digging inside polygon.
- [ ] Convert raster to shapefile by GIS instead of findContours in OpenCV.
- [ ] Update plugin's UI.
- [ ] Accelerate, etc.
