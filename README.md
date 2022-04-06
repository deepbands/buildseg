<div align="center">
    <article style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
        <p align="center"><img width="300" src="./docs/img/logo.png" /></p>
        <h1 style="width: 100%; text-align: center;">buildseg: QGIS plugin for building extraction</h1>
    </article>
    English | <a href="./docs/README_CN.md">简体中文</a>
</div>
<br/>

[![Python 3.8](https://img.shields.io/badge/python-3.8-yellow.svg)](https://www.python.org/downloads/release/python-380/) [![QGIS 3.16.11](https://img.shields.io/badge/qgis-3.16.11+-green.svg)](https://www.qgis.org/) ![license](https://img.shields.io/github/license/deepbands/buildseg) ![release](https://img.shields.io/badge/release-v0.2-red.svg)

buildseg is a Building Extraction plugin for QGIS based on ONNX (Use PaddlePaddle to train and convert to ONNX), and it using the semantic segmentation ability provided by paddleseg, large areas can be extracted and spliced. At present, automatic downloading of raster images and building extraction are added, and users need to register in mapbox and record Token.

![show](https://user-images.githubusercontent.com/71769312/159407433-96052623-3837-41dd-86b8-003da15b59eb.gif)

*\*Noto: The raster is downloaded from mapbox according to the vector range, and model is SegFormer_B2.*

## How to use

1. Download and install [QGIS](https://www.qgis.org/en/site/) and clone the repo:
``` git
git clone git@github.com:deepbands/buildseg.git
```

2. Install requirements:
   - Enter the folder and install dependent libraries using OSGeo4W shell (Open As Administrator) :
   ``` shell
   cd buildseg
   pip install -r requirements.txt
   ```
   - Or open OSGeo4W shell as administrator and enter:
    ``` shell
    pip install opencv-python onnx onnxruntime --user
    ```

3. Copy folder named buildseg in QGIS configuration folder and choose the plugin from plugin manager in QGIS (If not appeared restart QGIS).
   - You can know this folder from QGIS Setting Menu at the top-left of QGIS UI `[Settings] > [User Profiles] > [Open Active Profile Folder]`.
   - Go to `python\plugins` then paste the buildseg folder.
   - Full path should be like : `C:\Users\$USER\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\buildseg`.

4. Open QGIS, load your raster and select the ONNX file (`*.onnx`) then click `ok`. 

## Model and Parameter

- mIoU from PaddlePaddle and other from ONNX.
- Train / Eval (5k) Dataset: [AI Studio](https://aistudio.baidu.com/aistudio/datasetdetail/102929).
- Run time test environment: [Win10] / [i7-10750H] / [RTX 2060] and test image: [Baidu drive](https://pan.baidu.com/s/14novqjR7gEXVCLwZkxqepw) | [Google drive](https://drive.google.com/file/d/1aySfvIzAnQDkVKUkFmyNq8O7p2S3IhUl/view?usp=sharing).

|                        Model                         | Backbone  | Resolution |  mIoU  | Params(MB) | Running Time(s) |                        Static Weight                         |
| :--------------------------------------------------: | :-------: | :--------: | :----: | :--------: | :-------------: | :----------------------------------------------------------: |
|    [OCRNet](https://arxiv.org/pdf/1909.11065.pdf)    | HRNet_W18 |  512x512   | 89.38% |   46.49    |     39.090      | [Baidu drive](https://pan.baidu.com/s/1ZOy4HpC2TPWIGSGU0DX2UQ) \| [Google drive](https://drive.google.com/file/d/1wKC5PxroqDzrUz9nOFuA1KOFlv18MqS9/view?usp=sharing) |
| [SegFormer_B2](https://arxiv.org/pdf/2112.08275.pdf) |     -     |  512x512   | 89.47% |   104.56   |     59.498      | [Baidu drive](https://pan.baidu.com/s/1knnge-bRkXIhzS-RRTJ8lQ) \| [Google drive](https://drive.google.com/file/d/1TXF2T6LORRyDoCmkwmZsxjo0Km9BwuAK/view?usp=sharing) |
|  [BiSeNet_V2](https://arxiv.org/pdf/2004.02147.pdf)  |     -     |  512x512   | 84.61% |    8.94    |      7.004      | [Baidu drive](https://pan.baidu.com/s/1pDBLc7MoLaBERKe2I536sA) \| [Google drive](https://drive.google.com/file/d/1SYwzWBU4wMJfzOf83Tboe7_P7TLW44xw/view?usp=sharing) |

*\*Noto : All of Baidu drive's code is `band`.*

## How to Train

This work is in progress, at present, the relevant documents are as follows :

- [\* How to make dataset in QGIS](https://github.com/deepbands/deep-learning-datasets-maker)

- [How to train your data](./docs/train/train.md)
- [How to convert to ONNX weight](./docs/train/to_onnx.md)
