# **如何训练自己的数据**

这是来自[buildseg](https://github.com/deepbands/buildseg)的模型训练部分代码，通过这里的平台和代码可以训练自己的模型，再将模型转化为静态图模型，即可在buildseg中使用自己的模型。

在AI Studio中需要执行前两步，参考[AI Studio项目](https://aistudio.baidu.com/studio/project/partial/verify/3173288/089bf94fa80945cdbef2f32b2e21eeb4)。在本地只需要准备好数据后从第三步开始执行，`label.py`位于trained/tools文件夹中。

## 1 安装依赖

我们应该先安装paddleseg用于图像分割的训练。


```python
! pip install -q paddleseg
```

## 2 解压数据

数据在启动前可以通过项目页面的 “修改” -> “下一步” 找到数据集，上传自己的数据集到AI Studio就可以使用了，数据集放在`data`目录中，这个目录在每次退出后会清除除数据压缩包外的所有文件。如果我们数据较大，可以解压到`data`中，避免数据量过多无法保存。


```python
# 数据解压
! mkdir -p /home/aistudio/data/dataset
! zip -s 0 -q /home/aistudio/data/data102929/rs_builds.zip --out /home/aistudio/data/rs_builds_all.zip
! unzip -oq /home/aistudio/data/rs_builds_all.zip -d /home/aistudio/data/dataset
```

## 3 划分数据列表

将`train2.txt`中的文件名取出，打乱顺序，抽出5000份数据用于评估，其他数据用于训练，构造数据列表，保存为`train.txt`以及`val.txt`。


```python
# 划分数据集
import os
import os.path as osp
import random


gt_folder = "/home/aistudio/data/dataset/rs_builds/gt"
random.seed(24)
names = os.listdir(gt_folder)
random.shuffle(names)
print("数据量: ", len(names))
with open("data/dataset/rs_builds/train.txt", "w") as tf:
    with open("data/dataset/rs_builds/val.txt", "w") as vf:
        for idx, name in enumerate(names):
            name = name.split(".")[0]
            if idx < 5000:  # 5000份数据用于评估
                vf.write("img/" + name + ".jpg gt/" + name + ".png\n")
            else:
                tf.write("img/" + name + ".jpg gt/" + name + ".png\n")
print("完成")
```

## 4 包导入

主要可以修改的地方在于可以导入不同的模型。有哪些模型可以参考[这里](https://github.com/PaddlePaddle/PaddleSeg/blob/release/2.3/docs/model_zoo_overview.md)。


```python
import paddle
import paddleseg.transforms as T
from paddleseg.datasets import Dataset
from paddleseg.models.segformer import SegFormer_B2  # segformer
# from paddleseg.models import OCRNet, HRNet_W18  # OCRNet
from paddleseg.models.losses import MixedLoss, BCELoss, DiceLoss, LovaszHingeLoss
from paddleseg.core import train, evaluate
```

## 5 数据集建立

其中是对数据的路径及使用的数据增强方式进行设置。其中包含了翻转旋转等数据增强操作，以及需要设置相对应的类别数。


```python
# 建立训练数据集
train_transforms = [
    T.RandomHorizontalFlip(),
    T.RandomVerticalFlip(),
    T.RandomRotation(),
    T.RandomScaleAspect(),
    T.RandomBlur(),
    T.Resize(target_size=(512, 512)),
    T.Normalize()
]
train_dataset = Dataset(
    transforms=train_transforms,
    dataset_root="data/dataset/rs_builds",
    num_classes=2,
    mode="train",
    train_path="data/dataset/rs_builds/train.txt",
    separator=" "
)

# 建立评估数据集
val_transforms = [
    T.Resize(target_size=(512, 512)),
    T.Normalize()
]
val_dataset = Dataset(
    transforms=val_transforms,
    dataset_root="data/dataset/rs_builds",
    num_classes=2,
    mode="val",
    train_path="data/dataset/rs_builds/val.txt",
    separator=" "
)
```

## \* 检查数据

可以通过这一步检查数据集的形状和标签范围是否正确。


```python
import numpy as np


for img, lab in val_dataset:
    print(img.shape, lab.shape)
    print(np.unique(lab))
```

## 6 训练参数设置

从上到下分别是学习率、训练轮数、批大小、模型设置、学习率衰减设置、优化器设置及损失函数设置。这里可以参考[API文档](https://github.com/PaddlePaddle/PaddleSeg/blob/release/2.3/docs/apis/README_CN.md)。


```python
base_lr = 3e-5
epochs = 2
batch_size = 16
iters = epochs * len(train_dataset) // batch_size

model = SegFormer_B2(num_classes=2,
                     pretrained="output/best_model/model.pdparams")

# model = OCRNet(num_classes=2,
#                backbone=HRNet_W18(),
#                backbone_indices=[0],
#                pretrained="output/best_model/model.pdparams")

# lr = paddle.optimizer.lr.LinearWarmup(base_lr, warmup_steps=iters // epochs, start_lr=base_lr / 10, end_lr=base_lr)
lr = paddle.optimizer.lr.PolynomialDecay(base_lr, decay_steps=iters // epochs, end_lr=base_lr / 5)
optimizer = paddle.optimizer.AdamW(lr, beta1=0.9, beta2=0.999, weight_decay=0.01, parameters=model.parameters())
losses = {}
losses["types"] = [MixedLoss([BCELoss(), DiceLoss(), LovaszHingeLoss()], [2, 1, 1])]  #  * 2
losses["coef"] = [1]  # [1, 0.4]
```

## 7 开始训练

一般来说，这里仅仅需要修改`save_dir`为自己的保存路径即可，还可以通过`save_interval`设置保存评估的间隔数。


```python
model.train()

train(
    model=model,
    train_dataset=train_dataset,
    val_dataset=val_dataset,
    optimizer=optimizer,
    save_dir="output_segformer",
    iters=iters,
    batch_size=batch_size,
    save_interval=iters // 5,
    log_iters=10,
    num_workers=0,
    losses=losses,
    use_vdl=True)
```

## 8 模型评估

直接运行即可。


```python
model.eval()

evaluate(
    model,
    val_dataset)
```

## \* 当前结果

### OCRNet-HRNet_W18

```shell
[INFO]	[EVAL] #Images: 5000 mIoU: 0.8938 Acc: 0.9582 Kappa: 0.8863 
[INFO]	[EVAL] Class IoU: [0.9464 0.8412]
[INFO]	[EVAL] Class Acc: [0.987  0.8733]
```

### SegFormer_B2

```shell
[INFO]	[EVAL] #Images: 5000 mIoU: 0.8947 Acc: 0.9585 Kappa: 0.8874 
[INFO]	[EVAL] Class IoU: [0.9466 0.8429]
[INFO]	[EVAL] Class Acc: [0.9889 0.8701]

```

### BiSeNet_V2

```shell
[INFO]	[EVAL] #Images: 5000 mIoU: 0.8461 Acc: 0.9359 Kappa: 0.8303 
[INFO]	[EVAL] Class IoU: [0.9179 0.7742]
[INFO]	[EVAL] Class Acc: [0.9844 0.8065]
```
