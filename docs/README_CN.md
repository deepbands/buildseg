<div align="center">
    <article style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
        <p align="center"><img width="300" src="./img/logo.png" /></p>
        <h1 style="width: 100%; text-align: center;">buildseg：用于建筑提取的QGIS插件</h1>
    </article>
    <a href="../README.md">English</a> | 简体中文
</div>

<br/>

[![Python 3.8](https://img.shields.io/badge/python-3.8-yellow.svg)](https://www.python.org/downloads/release/python-380/) [![QGIS 3.16.11](https://img.shields.io/badge/qgis-3.16.11+-green.svg)](https://www.qgis.org/) ![license](https://img.shields.io/github/license/deepbands/buildseg) ![release](https://img.shields.io/badge/release-v0.2-red.svg)

buildseg是一个基于ONNX的用于建筑提取的QGIS插件（使用PaddlePaddle训练并转为ONNX），使用PaddleSeg提供的语义分割能力，可以对大片区域进行分块提取并拼接。当前新增了自动下载栅格影像并进行建筑提取，用户需要在Mapbox进行注册并记录Token。

![show](https://user-images.githubusercontent.com/71769312/159407433-96052623-3837-41dd-86b8-003da15b59eb.gif)

*\*说明：栅格根据矢量范围从Mapbox下载，且使用的模型为SegFormer_B2。*

## 如何使用

1. 下载并安装[QGIS](https://www.qgis.org/en/site/)，然后克隆这个项目：
``` git
git clone git@github.com:deepbands/buildseg.git
```

2. 安装依赖：
   - 进入项目文件夹并且使用OSGeo4W shell（使用管理员打开）安装依赖库：
   ``` shell
   cd buildseg
   pip install -r requirements.txt
   ```
   - 或者直接使用管理员权限打开OSGeo4W shell并且输入：
    ``` shell
    pip install opencv-python onnx onnxruntime --user
    ```

3. 复制buildseg文件夹到QGIS配置文件夹并在QGIS的插件管理中选择此插件（如果未显示，请重新启动QGIS）。
   - 你可以通过QGIS界面中左上方的菜单知道你的配置文件夹路径 `[设置] > [用户配置] > [打开当前配置文件夹]` 。
   - 进入 `python\plugins` 然后粘贴buildseg文件夹。
   - 完整的路径应该如下：`C:\Users\$USER\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\buildseg`。

4. 打开QGIS，导入栅格图像并且选择ONNX文件（`*.onnx`）然后点击`ok`。

## 模型和参数

- mIoU从PaddlePaddle模型测出，其他的参数由ONNX模型获得。
- 训练 / 评估 （5k）数据：[AI Studio](https://aistudio.baidu.com/aistudio/datasetdetail/102929)。
- 运行耗时的测试环境：[Win10] / [i7-10750H] / [RTX 2060] ，测试数据：[百度云盘](https://pan.baidu.com/s/14novqjR7gEXVCLwZkxqepw) | [谷歌云盘](https://drive.google.com/file/d/1aySfvIzAnQDkVKUkFmyNq8O7p2S3IhUl/view?usp=sharing)。

|                         模型                         | 骨干网络  | 分辨率  | 平均交并比 | 参数(MB) | 运行耗时(s) |                           静态权重                           |
| :--------------------------------------------------: | :-------: | :-----: | :--------: | :------: | :---------: | :----------------------------------------------------------: |
|    [OCRNet](https://arxiv.org/pdf/1909.11065.pdf)    | HRNet_W18 | 512x512 |   89.38%   |  46.49   |   39.090    | [百度云盘](https://pan.baidu.com/s/1ZOy4HpC2TPWIGSGU0DX2UQ) \| [谷歌云盘](https://drive.google.com/file/d/1wKC5PxroqDzrUz9nOFuA1KOFlv18MqS9/view?usp=sharing) |
| [SegFormer_B2](https://arxiv.org/pdf/2112.08275.pdf) |     -     | 512x512 |   89.47%   |  104.56  |   59.498    | [百度云盘](https://pan.baidu.com/s/1knnge-bRkXIhzS-RRTJ8lQ) \| [谷歌云盘](https://drive.google.com/file/d/1TXF2T6LORRyDoCmkwmZsxjo0Km9BwuAK/view?usp=sharing) |
|  [BiSeNet_V2](https://arxiv.org/pdf/2004.02147.pdf)  |     -     | 512x512 |   84.61%   |   8.94   |    7.004    | [百度云盘](https://pan.baidu.com/s/1pDBLc7MoLaBERKe2I536sA) \| [谷歌云盘](https://drive.google.com/file/d/1SYwzWBU4wMJfzOf83Tboe7_P7TLW44xw/view?usp=sharing) |

*\*说明 ：所有百度网盘的提取码均为`band`.*

## 如何训练

这项工作正在进行中，目前相关的文档如下：

- [\* 如何在QGIS中制作数据集](https://github.com/deepbands/deep-learning-datasets-maker)

- [如何训练自己的数据](./docs/train/train_CN.md)
- [如何转换为ONNX模型](./docs/train/to_onnx_CN.md)
