# **How to train your data in AI Studio（如何在AI Studio训练自己的数据）**

This is the model training code from [buildseg](https://github.com/deepbands/buildseg). You can train your own model through the platform and code here, and then convert the model into a static graph model, so you can use your own model in buildseg. The following contents and can be found in [AI Studio project](https://aistudio.baidu.com/studio/project/partial/verify/3173288/089bf94fa80945cdbef2f32b2e21eeb4).

这是来自[buildseg](https://github.com/deepbands/buildseg)的模型训练部分代码，通过这里的平台和代码可以训练自己的模型，再将模型转化为静态图模型，即可在buildseg中使用自己的模型。下面的内容和可以[AI Studio的项目](https://aistudio.baidu.com/studio/project/partial/verify/3173288/089bf94fa80945cdbef2f32b2e21eeb4)中找到。

## 1 Installation dependency（安装依赖）

We should first install paddleseg for image segmentation training.

我们应该先安装paddleseg用于图像分割的训练。


```python
! pip install -q paddleseg
```

## 2 Decompress data（解压数据）

Before starting the data, you can find the data set through "modify" -> "next" on the project page, and upload your own data set to AI Studio for use. The data set is placed in the `data` directory, which will clear all files except the data compression package after each exit. If our data is large, we can decompress it into `data` to avoid too much data to save.

数据在启动前可以通过项目页面的 “修改” -> “下一步” 找到数据集，上传自己的数据集到AI Studio就可以使用了，数据集放在`data`目录中，这个目录在每次退出后会清除除数据压缩包外的所有文件。如果我们数据较大，可以解压到`data`中，避免数据量过多无法保存。


```python
# # Decompress data 
# # 数据解压
# # If there is only one compressed package in the dataset, you can decompress it directly
# # 如果数据集中只有一个压缩包，可以直接解压

# # ! mkdir -p /home/aistudio/data/dataset
# # ! unzip -oq /home/aistudio/data/data102929/rs_building_x.zip -d /home/aistudio/data/dataset


# # Similar to this data, there are multiple compressed packages, which can be decompressed circularly
# # 类似于这个数据有多个压缩包，可以循环解压

# import os
# import os.path as osp
# from tqdm import tqdm
# from zipfile import ZipFile


# def _mkdir_p(folder_path):
#     if not osp.exists(folder_path):
#         os.makedirs(folder_path)


# def unzip_folders(src, dst):
#     _mkdir_p(dst)
#     ps = os.listdir(src)
#     for p in tqdm(ps):
#         z = ZipFile(osp.join(src, p), 'r')
#         z.extractall(path=dst)
#         z.close()
#     print("Decompression complete（解压完成）")


# dataset_path = "/home/aistudio/data/data102929"
# unzip_path = "/home/aistudio/data/dataset"
# unzip_folders(dataset_path, unzip_path)
```

## 3 Data filtering （数据筛选）

The code here can remove the image with a large area label as the background from the data list, and the data names that meet the requirements will be retained in `train2.txt`.


通过这里的代码可以将大面积标签为背景的图像剔除在数据列表之外，符合要求的数据名称则会保留在`train2.txt`中。


```python
# # Data filtering
# # 数据筛选
# from label import get_img_file


# label = get_img_file('/home/aistudio/data/dataset/img')
```

## 4 Split dataset list（划分数据列表）

Add `train2.txt` file name is taken out, the order is disrupted, 5000 pieces of data are taken out for evaluation, other data are used for training, data list is constructed and saved as `train.txt` and `val.txt`.

将`train2.txt`中的文件名取出，打乱顺序，抽出5000份数据用于评估，其他数据用于训练，构造数据列表，保存为`train.txt`以及`val.txt`。


```python
# # Split dataset list
# # 划分数据集
# import os
# import os.path as osp
# import random


# train2_txt = "/home/aistudio/train2.txt"
# random.seed(24)
# # names = os.listdir(gt_folder)
# names = []
# with open(train2_txt, "r") as t2f:
#     names = t2f.readlines()
# random.shuffle(names)
# print("Data volume（数据量）: ", len(names))
# with open("data/dataset/train.txt", "w") as tf:
#     with open("data/dataset/val.txt", "w") as vf:
#         for idx, name in enumerate(names):
#             name = name.strip()
#             if idx < 5000:  # 5000 data for evaluation（5000份数据用于评估）
#                 vf.write("img/" + name + ".jpg gt/" + name + ".png\n")
#             else:
#                 tf.write("img/" + name + ".jpg gt/" + name + ".png\n")
# print("Finished（完成）")
```

## 5 Package import（包导入）

The main thing you can modify is that you can import different models. What models can you refer to [here](https://github.com/PaddlePaddle/PaddleSeg/blob/release/2.3/docs/model_zoo_overview.md).

*\*Note: Just Chinese now.*

主要可以修改的地方在于可以导入不同的模型。有哪些模型可以参考[这里](https://github.com/PaddlePaddle/PaddleSeg/blob/release/2.3/docs/model_zoo_overview.md)。

*\*说明：当前只有中文说明。*


```python
import paddle
import paddleseg.transforms as T
from paddleseg.datasets import Dataset
# from paddleseg.models import OCRNet, HRNet_W18  # OCRNet
from paddleseg.models.segformer import SegFormer_B2  # segformer
from paddleseg.models.losses import MixedLoss, BCELoss, DiceLoss, LovaszHingeLoss
from paddleseg.core import train, evaluate
```

## \* Label processing（标签处理）

This is not necessary. The following is a data preprocessing method added, which will convert 0-255 labels to 0-1, and when there are 3 channels in the label, only one channel will be taken.

这不是必要的，下面是添加了一个数据预处理的方法，它将把0-255的标签转换为0-1的，并且当标签中有3个通道时，只取其中一个通道。


```python
import numpy as np
from paddleseg.cvlibs import manager


@manager.TRANSFORMS.add_component
class InitMask:
    def __init__(self):
        pass

    def __call__(self, im, label=None):
        label = np.clip(label, 0, 1)
        if label is None:
            return (im, )
        else:
            if len(label.shape) == 3:
                label = np.mean(label, axis=-1).astype("uint8")
            return (im, label)
```

## 6 Data set establishment（数据集建立）

Where is to set the data path and the data enhancement method used. One problem is the final `mode="train"` of `val_dataset`. If the label needs to use `initmask()`, the label will be processed only when `mode="train"`; When `mode="Val"`, the data enhancement method will be invalid for the label.

其中是对数据的路径及使用的数据增强方式进行设置。有一个问题在于最后的`val_dataset`的`mode="train"`。如果标签需要使用`InitMask()`，则只有在`mode="train"`的情况下才会处理标签；当`mode="val"`，数据增强的方法将对标签无效。


```python
# Build the training set
# 建立训练数据集
train_transforms = [
    InitMask(),  # This is not necessary（这不是必要的）
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
    dataset_root="data/dataset",
    num_classes=2,
    mode="train",
    train_path="data/dataset/train.txt",
    separator=" "
)

# Build validation set
# 建立评估数据集
val_transforms = [
    InitMask(),
    T.Resize(target_size=(512, 512)),
    T.Normalize()
]
val_dataset = Dataset(
    transforms=val_transforms,
    dataset_root="data/dataset",
    num_classes=2,
    mode="train",  # If your data does not need `initmask()`, please use "val"（如果你的数据不需要`InitMask()`，请使用val"）
    train_path="data/dataset/val.txt",
    separator=" "
)
```

## \* Check dataset（检查数据）

You can use this step to check whether the shape and label range of the dataset are correct.

可以通过这一步检查数据集的形状和标签范围是否正确。


```python
# for img, lab in val_dataset:
#     print(img.shape, lab.shape)
#     print(np.unique(lab))
```

## 7 Training parameter setting（训练参数设置）

From top to bottom are learning rate, number of training rounds, batch size, model setting, learning rate attenuation setting, optimizer setting and loss function setting. You can refer to [API documentation](https://github.com/PaddlePaddle/PaddleSeg/blob/release/2.3/docs/apis/README.md) here.

从上到下分别是学习率、训练轮数、批大小、模型设置、学习率衰减设置、优化器设置及损失函数设置。这里可以参考[API文档](https://github.com/PaddlePaddle/PaddleSeg/blob/release/2.3/docs/apis/README_CN.md)。


```python
base_lr = 3e-5
epochs = 2
batch_size = 16
iters = epochs * len(train_dataset) // batch_size

# model = OCRNet(num_classes=2,
#                backbone=HRNet_W18(),
#                backbone_indices=[0],
#                pretrained="output/best_model/model.pdparams")

model = SegFormer_B2(num_classes=2,
                     pretrained="output_segformer/best_model/model.pdparams")

# lr = paddle.optimizer.lr.LinearWarmup(base_lr, warmup_steps=iters // epochs, start_lr=base_lr / 10, end_lr=base_lr)
lr = paddle.optimizer.lr.PolynomialDecay(base_lr, decay_steps=iters // epochs, end_lr=base_lr / 5)
optimizer = paddle.optimizer.AdamW(lr, beta1=0.9, beta2=0.999, weight_decay=0.01, parameters=model.parameters())
losses = {}
losses["types"] = [MixedLoss([BCELoss(), DiceLoss(), LovaszHingeLoss()], [2, 1, 1])]  #  * 2
losses["coef"] = [1]  # [1, 0.4]
```

## 8 Start training（开始训练）

Generally speaking, you only need to modify `save_dir` can be your own save path, or through `save_interval` sets the number of intervals to save the evaluation.

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

## 9 Model evaluation（模型评估）

Just run it directly.

直接运行即可。


```python
# model.eval()

# evaluate(
#     model,
#     val_dataset)
```

## 10 Save and convert to static graph model（保存及转换为静态图模型）

View the folder where the model is saved, and click the `pdparams` file under the `best_model` is downloaded locally, and then this dynamic graph parameter can be converted into a static graph model locally using paddleseg. For relevant operations, please refer to [here](to_static).

*\*Note: Just Chinese now.*

查看保存模型的文件夹，将`best_model`下的`pdparams`文件下载到本地，然后可以在本地使用PaddleSeg将此动态图参数转为静态图模型，相关操作可以参考[这里](to_static)。

*\*说明：当前只有中文说明。*

## \* Current results（当前结果）

### OCRNet-HRNet_W18
```
2021-12-11 09:44:44 [INFO]	[EVAL] #Images: 5000 mIoU: 0.8938 Acc: 0.9582 Kappa: 0.8863 
2021-12-11 09:44:44 [INFO]	[EVAL] Class IoU: 
[0.9464 0.8412]
2021-12-11 09:44:44 [INFO]	[EVAL] Class Acc: 
[0.987  0.8733]
```

### SegFormer_B2
```
2021-12-15 23:30:32 [INFO]	[EVAL] #Images: 5000 mIoU: 0.8947 Acc: 0.9585 Kappa: 0.8874 
2021-12-15 23:30:32 [INFO]	[EVAL] Class IoU: 
[0.9466 0.8429]
2021-12-15 23:30:32 [INFO]	[EVAL] Class Acc: 
[0.9889 0.8701]

```
