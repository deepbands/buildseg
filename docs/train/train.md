# **How to train your data**

This is the model training code from [buildseg](https://github.com/deepbands/buildseg). You can train your own model through the platform and code here, and then convert the model into a static graph model, so you can use your own model in buildseg. 

The first 2 steps need to be performed in AI studio. Refer to [AI studio project](https://aistudio.baidu.com/studio/project/partial/verify/3173288/089bf94fa80945cdbef2f32b2e21eeb4). In local, you only need to prepare the data and start from step 3, `label.py` is located in the trained/tools folder.

## 1 Installation dependency

We should first install paddleseg for image segmentation training.


```python
! pip install -q paddleseg
```

## 2 Decompress data (in AI Studio)

Before starting the data, you can find the data set through "modify" -> "next" on the project page, and upload your own data set to AI Studio for use. The data set is placed in the `data` directory, which will clear all files except the data compression package after each exit. If our data is large, we can decompress it into `data` to avoid too much data to save.


```python
# Decompress data
! mkdir -p /home/aistudio/data/dataset
! zip -s 0 -q /home/aistudio/data/data102929/rs_builds.zip --out /home/aistudio/data/rs_builds_all.zip
! unzip -oq /home/aistudio/data/rs_builds_all.zip -d /home/aistudio/data/dataset
```

## 3 Split dataset list

Add `train2.txt` file name is taken out, the order is disrupted, 5000 pieces of data are taken out for evaluation, other data are used for training, data list is constructed and saved as `train.txt` and `val.txt`.


```python
# Split dataset list
import os
import os.path as osp
import random


gt_folder = "/home/aistudio/data/dataset/rs_builds/gt"
random.seed(24)
names = os.listdir(gt_folder)
random.shuffle(names)
print("Data volume: ", len(names))
with open("data/dataset/rs_builds/train.txt", "w") as tf:
    with open("data/dataset/rs_builds/val.txt", "w") as vf:
        for idx, name in enumerate(names):
            name = name.split(".")[0]
            if idx < 5000:  # 5000 data for evaluation
                vf.write("img/" + name + ".jpg gt/" + name + ".png\n")
            else:
                tf.write("img/" + name + ".jpg gt/" + name + ".png\n")
print("Finished")
```

## 4 Package import

The main thing you can modify is that you can import different models. What models can you refer to [here](https://github.com/PaddlePaddle/PaddleSeg/blob/release/2.3/docs/model_zoo_overview.md).

*\*Note: Just Chinese now.*


```python
import paddle
import paddleseg.transforms as T
from paddleseg.datasets import Dataset
from paddleseg.models.segformer import SegFormer_B2  # segformer
# from paddleseg.models import OCRNet, HRNet_W18  # OCRNet
from paddleseg.models.losses import MixedLoss, BCELoss, DiceLoss, LovaszHingeLoss
from paddleseg.core import train, evaluate
```

## 5 Data set establishment

Where is to set the data path and the data enhancement method used. It includes data enhancement operations such as flip and rotation, and the number of classes to be set.


```python
# Build the training set
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

# Build validation set
val_transforms = [
    T.Resize(target_size=(512, 512)),
    T.Normalize()
]
val_dataset = Dataset(
    transforms=val_transforms,
    dataset_root="data/rs_builds/dataset",
    num_classes=2,
    mode="val",
    train_path="data/dataset/rs_builds/val.txt",
    separator=" "
)
```

## \* Check dataset

You can use this step to check whether the shape and label range of the dataset are correct.


```python
import numpy as np


for img, lab in val_dataset:
    print(img.shape, lab.shape)
    print(np.unique(lab))
```

## 6 Training parameter setting

From top to bottom are learning rate, number of training rounds, batch size, model setting, learning rate attenuation setting, optimizer setting and loss function setting. You can refer to [API documentation](https://github.com/PaddlePaddle/PaddleSeg/blob/release/2.3/docs/apis/README.md) here.


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

## 7 Start training

Generally speaking, you only need to modify `save_dir` can be your own save path, or through `save_interval` sets the number of intervals to save the evaluation.


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

## 8 Model evaluation

Just run it directly.


```python
model.eval()

evaluate(
    model,
    val_dataset)
```

## \* Current results

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
