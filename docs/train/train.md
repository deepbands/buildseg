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
# # Decompress data 
# # If there is only one compressed package in the dataset, you can decompress it directly

# # ! mkdir -p /home/aistudio/data/dataset
# # ! unzip -oq /home/aistudio/data/data102929/rs_building_x.zip -d /home/aistudio/data/dataset


# # Similar to this data, there are multiple compressed packages, which can be decompressed circularly

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
#     print("Decompression complete")


# dataset_path = "/home/aistudio/data/data102929"
# unzip_path = "/home/aistudio/data/dataset"
# unzip_folders(dataset_path, unzip_path)
```

## 3 Data filtering

The code here can remove the image with a large area label as the background from the data list, and the data names that meet the requirements will be retained in `train2.txt`.


```python
# Data filtering
from label import get_img_file


label = get_img_file('/home/aistudio/data/dataset/img')
```

## 4 Split dataset list

Add `train2.txt` file name is taken out, the order is disrupted, 5000 pieces of data are taken out for evaluation, other data are used for training, data list is constructed and saved as `train.txt` and `val.txt`.


```python
# Split dataset list
import os
import os.path as osp
import random


train2_txt = "/home/aistudio/train2.txt"
random.seed(24)
# names = os.listdir(gt_folder)
names = []
with open(train2_txt, "r") as t2f:
    names = t2f.readlines()
random.shuffle(names)
print("Data volume: ", len(names))
with open("data/dataset/train.txt", "w") as tf:
    with open("data/dataset/val.txt", "w") as vf:
        for idx, name in enumerate(names):
            name = name.strip()
            if idx < 5000:  # 5000 data for evaluation
                vf.write("img/" + name + ".jpg gt/" + name + ".png\n")
            else:
                tf.write("img/" + name + ".jpg gt/" + name + ".png\n")
print("Finished")
```

## 5 Package import

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

## 6 Data set establishment

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
    dataset_root="data/dataset",
    num_classes=2,
    mode="train",
    train_path="data/dataset/train.txt",
    separator=" "
)

# Build validation set
val_transforms = [
    InitMask(),
    T.Resize(target_size=(512, 512)),
    T.Normalize()
]
val_dataset = Dataset(
    transforms=val_transforms,
    dataset_root="data/dataset",
    num_classes=2,
    mode="val",
    train_path="data/dataset/val.txt",
    separator=" "
)
```

## \* Check dataset

You can use this step to check whether the shape and label range of the dataset are correct.


```python
for img, lab in val_dataset:
    print(img.shape, lab.shape)
    print(np.unique(lab))
```

## 7 Training parameter setting

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

## 8 Start training

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

## 9 Model evaluation

Just run it directly.


```python
model.eval()

evaluate(
    model,
    val_dataset)
```

## 10 Save and convert to static graph model

View the folder where the model is saved, and click the `pdparams` file under the `best_model` is downloaded locally, and then this dynamic graph parameter can be converted into a static graph model locally using paddleseg. For relevant operations, please refer to [here](to_static.md).

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
