<div align="center">
    <article style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
        <p align="center"><img width="300" src="./docs/img/logo.png" /></p>
        <h1 style="width: 100%; text-align: center;">buildseg: QGIS plugin for building extraction</h1>
    </article>
    English | <a href="./docs/README_CN.md">简体中文</a>
</div>

<br/>

[![Python 3.8](https://img.shields.io/badge/python-3.8-yellow.svg)](https://www.python.org/downloads/release/python-380/) [![PaddlePaddle 2.2](https://img.shields.io/badge/paddlepaddle-2.2+-blue.svg)](https://www.paddlepaddle.org.cn/install/quick?docurl=/documentation/docs/en/install/pip/windows-pip_en.html) [![QGIS 3.16.11](https://img.shields.io/badge/qgis-3.16.11+-green.svg)](https://www.qgis.org/) ![license](https://img.shields.io/github/license/deepbands/buildseg) ![release](https://img.shields.io/badge/release-v0.1-red.svg)

buildseg is a Building Extraction plugin for QGIS based on PaddlePaddle, and it useing the semantic segmentation ability provided by paddleseg, large areas can be extracted and spliced.

![bs002](https://user-images.githubusercontent.com/71769312/146371414-8c325496-d9e2-4f1e-891f-97bf3ca07716.gif)

*\*Noto : raster's size is 4983x3475, and model is SegFormer_B2*.

## How to use

1. Download and install [QGIS](https://www.qgis.org/en/site/) and clone the repo :
``` git
git clone git@github.com:deepbands/buildseg.git
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

|                        Model                         | Backbone  | Resolution |  mIoU  | Params(MB) | Running Time(s) |                        Static Weight                         |
| :--------------------------------------------------: | :-------: | :--------: | :----: | :--------: | :-------------: | :----------------------------------------------------------: |
|    [OCRNet](https://arxiv.org/pdf/1909.11065.pdf)    | HRNet_W18 |  512x512   | 89.38% |    46.2    |     269.805     | [Baidu drive](https://pan.baidu.com/s/1aQVc3InoUmxoGKSHCitvBw) \| [Google drive](https://drive.google.com/file/d/1LkwvAfIWf_RO4ybSAc_7yLm4hNp_sWjD/view?usp=sharing) |
| [SegFormer_B2](https://arxiv.org/pdf/2112.08275.pdf) |     -     |  512x512   | 89.47% |   104.0    |     171.245     | [Baidu drive](https://pan.baidu.com/s/1QohTl65OmYOU__ESQjcAcg) \| [Google drive](https://drive.google.com/file/d/1Kihnb5yRK0-aNnD_ZHgWUmLJqMzJKq_L/view?usp=sharing) |
|  [BiSeNet_V2](https://arxiv.org/pdf/2004.02147.pdf)  |     -     |  512x512   | 84.61% |    8.9     |     49.493      |                       For testing now                        |

- \*Note : 

  - Run time test environment :

    |   System   |             CPU              |             GPU             |  Memory   | Image size  |
    | :--------: | :--------------------------: | :-------------------------: | :-------: | :---------: |
    | Windows 10 | Intel Core i7-10750H 2.60GHz | NVIDIA GeForce RTX 2060 6GB | 16GB DDR4 | 4983x3475x3 |

  - All of Baidu drive's code is : band.

- Train/Eval(5k) Dataset : [Link](https://aistudio.baidu.com/aistudio/datasetdetail/102929).
- Testing Dataset : [Baidu drive](https://pan.baidu.com/s/14novqjR7gEXVCLwZkxqepw) | [Google drive](https://drive.google.com/file/d/1aySfvIzAnQDkVKUkFmyNq8O7p2S3IhUl/view?usp=sharing).

- We have done all testing and development using : Tesla V100 32G in [AI Studio](https://aistudio.baidu.com/aistudio/index).

## How to Train

This work is in progress, at present, the relevant documents are as follows :

- [\* How to make dataset in QGIS](https://github.com/deepbands/deep-learning-datasets-maker)

- [How to train your data](./docs/train/train.md)
- [How to convert to static weight](./docs/train/to_static.md)

## TODO

### v0.2

- [x] Environment dependency package check.

- [x] Add another model, like Vision Transform.

- [x] Add note：
    - [x] About how to training your data in AI Studio / Local.
    - [x] About different model (paper's link).

- [x] Accelerate and reduce memory:
    - [x] PaddlePaddle setting.
    - [x] Add maximum pixelsize to calculate / using GDAL `translat / warp` to make raster smaller.
    - [x] Block stacking and saving.

- [ ] Test:
  - [x] On Windows 10/11.
  - [ ] On Linux.
  - [ ] On mac OS Big Sur+.

- [ ] Add online map tiles support:
	- [ ] Extract building on raster in memory.
	- [ ] Add vector range selection.
