# 转换为静态图模型

当我们使用AI Studio或者本地训练好之后，就可以从保存的文件夹得到动态图的参数文件，为`*.pdparams`。我们需要将其转变为静态图模型后，才能被buildseg所使用的。

## 文件准备

```shell
output
  ├── ocrnet_hrnet_w18_512x512.yml   # 网络及val预处理配置文件
  └── best_model.pdparams            # 保存的动态图参数
```

其中配置文件可根据网络定义时的参数，写成yml文件即可，如下对应：

- 网络代码：

  ```python
  model = OCRNet(num_classes=2,
                 backbone=HRNet_W18(),
                 backbone_indices=[0])
  ```

- 配置文件：

  ```yaml
  model:
    num_classes: 2
    type: OCRNet
    backbone:
      type: HRNet_W18
    backbone_indices: [0]
  ```

## 转换

确保正确安装PaddleSeg后，在PaddleSeg目录下执行如下命令，则预测模型会保存在output文件夹。

```shell
# 设置1张可用的卡
export CUDA_VISIBLE_DEVICES=0

# windows下请执行以下命令
# set CUDA_VISIBLE_DEVICES=0
python export.py \
       --config configs/bisenet/bisenet_cityscapes_1024x1024_160k.yml \
       --model_path bisenet/model.pdparams \
       --save_dir output
```

### 导出脚本参数解释

| 参数名         | 用途                                                         | 是否必选项 | 默认值                         |
| -------------- | ------------------------------------------------------------ | ---------- | ------------------------------ |
| config         | 配置文件                                                     | 是         | -                              |
| model_path     | 预训练权重的路径                                             | 否         | 配置文件中指定的预训练权重路径 |
| save_dir       | 保存预测模型的路径                                           | 否         | output                         |
| input_shape    | 设置导出模型的输入shape，比如传入`--input_shape 1 3 1024 1024`。如果不设置input_shape，默认导出模型的输入shape是[-1, 3, -1, -1] | 否         | None                           |
| with_softmax   | 在网络末端添加softmax算子。由于PaddleSeg组网默认返回logits，如果想要部署模型获取概率值，可以置为True | 否         | False                          |
| without_argmax | 是否不在网络末端添加argmax算子。由于PaddleSeg组网默认返回logits，为部署模型可以直接获取预测结果，我们默认在网络末端添加argmax算子 | 否         | False                          |

## 3. 预测模型文件

如下是导出的预测模型文件。

```shell
output
  ├── deploy.yaml            # 部署相关的配置文件，主要说明数据预处理的方式
  ├── model.pdmodel          # 预测模型的拓扑结构文件
  ├── model.pdiparams        # 预测模型的权重文件
  └── model.pdiparams.info   # 参数额外信息，一般无需关注
```