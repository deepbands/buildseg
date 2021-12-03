# buildseg
[![Python 3.8](https://img.shields.io/badge/python-3.8-red.svg)](https://www.python.org/downloads/release/python-360/) [![PaddlePaddle 2.2](https://img.shields.io/badge/paddlepaddle-2.2-green.svg)](https://www.python.org/downloads/release/python-360/) [![QGIS 3.16.11](https://img.shields.io/badge/qgis-3.16.11-blue.svg)](https://www.python.org/downloads/release/python-360/)

buildseg is a building extraction plugin of QGIS based on PaddlePaddle.

![gasd](https://user-images.githubusercontent.com/71769312/144436933-f22c6a14-706f-406b-ad04-c0e784ed317b.gif)

## How to use
1. Download and install QGIS and clone the repo:

``` git
git clone git@github.com:geoyee/buildseg.git
```

2. Enter the folder and install dependent libraries using OSGeo4W shell:

``` shell
cd buildseg
pip install -r requirements.txt
```

3. Copy folder named buildseg in QGIS configuration folder(?\default\python\plugins) and reload plugin.

4. Open QGIS and load raster, and use the plugin to select the parameter file(*.pdparams).

## Model and Parameter

| Model              | mIoU | Size(Pix) | Params(M) | Inference Time(ms) | Static Weight | Dygraph Weight |
| ------------------ | ---- | --------- | --------- | ------------------ | ------------- | -------------- |
| OCRNet (HRNet_W18) |      | 512x512   |           |                    |               |                |

## TODO

- [x] Extract building on 512x512 remote sensing images.
- [x] Extract building on big remote sensing images through sliding frame and splicing.
- [ ] Replace the model and parameters (large-scale data).
- [ ] Convert to static weight.
- [ ] Add a Jupyter Notebook(*.ipynb) about how to fine-tune it used other's dataset based on  PaddleSeg.
- [ ] Hole digging inside polygon.
- [ ] Convert raster to shapefile by GIS instead of findContours in OpenCV.
- [ ] Update plugin's UI.
- [ ] Accelerate, etc.
- [ ] Add another model, like Vision Transform.
