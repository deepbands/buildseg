<div align="center">
  <article style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
      <p align="center"><img width="300" src="./docs/img/logo.png" /></p>
      <h1 style="width: 100%; text-align: center;">buildseg</h1>
      <p>buildseg is a Building Extraction plugin for QGIS based on PaddlePaddle.</p>
  </article>
</div>

[![Python 3.8](https://img.shields.io/badge/python-3.8-red.svg)](https://www.python.org/downloads/release/python-360/) [![PaddlePaddle 2.2](https://img.shields.io/badge/paddlepaddle-2.2-green.svg)](https://www.python.org/downloads/release/python-360/) [![QGIS 3.16.11](https://img.shields.io/badge/qgis-3.16.11-blue.svg)](https://www.python.org/downloads/release/python-360/)

## Effect

![fds](https://user-images.githubusercontent.com/71769312/144746418-cdbb2d5a-32f8-49e3-bc42-d5d2d3e6810f.gif)

## How to use

1. Download and install [QGIS](https://www.qgis.org/en/site/) and clone the repo :
``` git
git clone git@github.com:geoyee/buildseg.git
```

2. Install requirements :
   - Enter the folder and install dependent libraries using OSGeo4W shell (Open As Administrator) :
   ``` shell
   cd buildseg
   pip install -r requirements.txt
   ```
   - Or open OSGeo4W shell as administrator and enter :
    ``` shell
    pip install opencv-python paddlepaddle>=2.2.0 paddleseg --user
    ```

3. Copy folder named buildseg in QGIS configuration folder and choose the plugin from plugin manager in QGIS (If not appeared restart QGIS).
   - You can know this folder from QGIS Setting Menu at the top-left of QGIS UI `Settings > User Profiles > Open Active Profile Folder` .
   - Go to `python/plugins` then paste the buildseg folder.
   - Full path should be like : `C:\Users\$USER\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\buildseg`.

4. Open QGIS, load your raster and select the parameter file ([*.pdiparams](https://cloud.a-boat.cn:2021/share/3xda5wmV)) then click `ok`. 

## Model and Parameter

| Model  | Backbone  | Resolution |  mIoU  | Params(MB) | Inference Time(ms) |                            Links                             |
| :----: | :-------: | :--------: | :----: | :--------: | :----------------: | :----------------------------------------------------------: |
| OCRNet | HRNet_W18 |  512x512   | 90.64% |    46.4    |         /          | [Static Weight](https://cloud.a-boat.cn:2021/share/3xda5wmV) |

- Train/Eval Dataset : [Link](https://aistudio.baidu.com/aistudio/datasetdetail/102929).
- We have done all testing and development using : Tesla V100 32G in [AI Studio](https://aistudio.baidu.com/aistudio/index).

## TODO

- [x] Extract building on 512x512 remote sensing images.
- [x] Extract building on big remote sensing images through splitting it into small tiles, extract buildings then mosaic it back (merge) to a full extent.
- [x] Replace the model and parameters (large-scale data).
- [x] Convert to static weight (\*.pdiparams) instead of dynamic model (\*.pdparams).
- [x] Add a Jupyter Notebook (\*.ipynb) about how to fine-tune parameters using other's datasets based on  PaddleSeg.
- [ ] Hole digging inside the polygons.
- [ ] Convert raster to Shapefile/GeoJson by GDAL/OGR (gdal.Polygonize) instead of findContours in OpenCV.
- [ ] Update plugin's UI :
    - [X] Add menu to select one raster file from QGIS opened raster layers.
    - [ ] Select the Parameter path one time (some buggy windows appear when importing the \*.pdiparams file).
    - [ ] Define the output path of the vector file (Direct Path or Temporary in the memory).
- [ ] Accelerate, etc.
- [ ] Add another model, like Vision Transform.
