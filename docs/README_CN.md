<div align="center">
    <article style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
        <p align="center"><img width="300" src="./img/logo.png" /></p>
        <h1 style="width: 100%; text-align: center;">buildseg：用于建筑提取的QGIS插件</h1>
    </article>
    <a href="../README.md">English</a> | 简体中文
</div>

<br/>

[![Python 3.8](https://img.shields.io/badge/python-3.8-yellow.svg)](https://www.python.org/downloads/release/python-380/) [![PaddlePaddle 2.2](https://img.shields.io/badge/paddlepaddle-2.2+-blue.svg)](https://www.paddlepaddle.org.cn/install/quick?docurl=/documentation/docs/zh/install/pip/windows-pip.html) [![QGIS 3.16.11](https://img.shields.io/badge/qgis-3.16.11+-green.svg)](https://www.qgis.org/) ![license](https://img.shields.io/github/license/deepbands/buildseg) ![release](https://img.shields.io/badge/release-v0.1-red.svg)

buildseg是一个基于PaddlePaddle的用于建筑提取的QGIS插件，使用PaddleSeg提供的语义分割能力，可以对大片区域进行分块提取并拼接。

![bs002](https://user-images.githubusercontent.com/71769312/146371414-8c325496-d9e2-4f1e-891f-97bf3ca07716.gif)

*\*说明：使用的栅格大小为 4983x3475，且使用的模型为SegFormer_B2。*

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
    pip install opencv-python paddlepaddle>=2.2.0 paddleseg --user
    ```

3. 复制buildseg文件夹到QGIS配置文件夹并在QGIS的插件管理中选择此插件（如果未显示，请重新启动QGIS）。
   - 你可以通过QGIS界面中左上方的菜单知道你的配置文件夹路径 `设置 > 用户配置 > 打开当前配置文件夹` 。
   - 进入 `python/plugins` 然后粘贴buildseg文件夹。
   - 完整的路径应该如下：`C:\Users\$USER\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\buildseg`。

4. 打开QGIS，导入栅格图像并且选择参数文件（[*.pdiparams](https://cloud.a-boat.cn:2021/share/3xda5wmV)）然后点击`ok`。

## 模型和参数

|                         模型                         | 骨干网络  | 分辨率  | 平均交并比 | 参数(MB) | 运行耗时(s) |                           静态权重                           |
| :--------------------------------------------------: | :-------: | :-----: | :--------: | :------: | :---------: | :----------------------------------------------------------: |
|    [OCRNet](https://arxiv.org/pdf/1909.11065.pdf)    | HRNet_W18 | 512x512 |   89.38%   |   46.2   |   269.805   | [百度云盘](https://pan.baidu.com/s/1aQVc3InoUmxoGKSHCitvBw) \| [谷歌云盘](https://drive.google.com/file/d/1LkwvAfIWf_RO4ybSAc_7yLm4hNp_sWjD/view?usp=sharing) |
| [SegFormer_B2](https://arxiv.org/pdf/2112.08275.pdf) |     -     | 512x512 |   89.47%   |  104.0   |   171.245   | [百度云盘](https://pan.baidu.com/s/1QohTl65OmYOU__ESQjcAcg) \| [谷歌云盘](https://drive.google.com/file/d/1Kihnb5yRK0-aNnD_ZHgWUmLJqMzJKq_L/view?usp=sharing) |
|  [BiSeNet_V2](https://arxiv.org/pdf/2004.02147.pdf)  |     -     | 512x512 |   84.61%   |   8.9    |   49.493    |                         目前用于测试                         |

- \*说明：

  - 运行耗时测试环境：

    |    系统    |            处理器            |            显卡             |   内存    |  图像大小   |
    | :--------: | :--------------------------: | :-------------------------: | :-------: | :---------: |
    | Windows 10 | Intel Core i7-10750H 2.60GHz | NVIDIA GeForce RTX 2060 6GB | 16GB DDR4 | 4983x3475x3 |

  - 所有的百度云盘提取码均为：band。

- 训练和评估（5千） 数据集：[链接](https://aistudio.baidu.com/aistudio/datasetdetail/102929)。

- 测试样张：[百度云盘](https://pan.baidu.com/s/14novqjR7gEXVCLwZkxqepw) | [谷歌云盘](https://drive.google.com/file/d/1aySfvIzAnQDkVKUkFmyNq8O7p2S3IhUl/view?usp=sharing).

- 训练和评估使用 : [AI Studio](https://aistudio.baidu.com/aistudio/index)提供的32G的Tesla V100。

## 如何训练

这项工作正在进行中，目前相关的文档如下：

- [\* 如何在QGIS中制作数据集](https://github.com/deepbands/deep-learning-datasets-maker)

- [如何训练自己的数据](./docs/train/train_CN.md)
- [如何转换为静态图模型](./docs/train/to_static_CN.md)

## 待办事项

### v0.2

- [x] 环境中依赖包的检查。
- [x] 添加例如ViT等的其他模型。
- [x] 添加描述说明：
    - [x] 关于如何在AI Studio以及本地训练自己的数据。
    - [x] 关于不同模型（论文链接）。
- [ ] 加速：
  - [x] 设置PaddlePaddle预测引擎。
  - [x] 添加最大像素值计算或者使用GDAL的`translat / warp`来减小栅格大小
  - [ ] 使用分块拼接和保存。
- [ ] 添加对在线地图瓦片的支持：
    - [ ] 可以对保存在内存中的栅格图像进行建筑提取。
    - [ ] 添加矢量边界的选择。
- [ ] 测试:
    - [x] 在 Windows 10/11上。
    - [ ] 在Linux上。
    - [ ] 在mac OS Big Sur+上。
