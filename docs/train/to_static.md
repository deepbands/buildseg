# Convert to static graph model

After using AI Studio or local training, we can get the parameter file of dynamic graph from the saved folder, which is ` *.pdparams`. But we need to convert it into a static graph model before it can be used by buildseg.

## Files preparation

```shell
output
  ├── ocrnet_hrnet_w18_512x512.yml   # Network and preprocessing profile
  └── best_model.pdparams            # Saved dynamic graph parameters
```

The config file can be written into a YML file according to the parameters during network definition, which corresponds to the following :

- Network :

  ```python
  model = OCRNet(num_classes=2,
                 backbone=HRNet_W18(),
                 backbone_indices=[0])
  ```

- config :

  ```yaml
  model:
    num_classes: 2
    type: OCRNet
    backbone:
      type: HRNet_W18
    backbone_indices: [0]
  ```

## Convert

Executing the following command in the PaddleSeg's directory after ensuring that PaddleSeg is installed correctly, and the prediction model will be saved in the output folder.

```shell
# Set an available card
# export CUDA_VISIBLE_DEVICES=0  # linux / macos
set CUDA_VISIBLE_DEVICES=0  # windows

# export static model
python export.py \
       --config configs/bisenet/bisenet_cityscapes_1024x1024_160k.yml \
       --model_path bisenet/model.pdparams \
       --save_dir output
```

### Parameter description

| Parameter's name | Purpose                                                      | Optional | Default                        |
| ---------------- | ------------------------------------------------------------ | -------- | ------------------------------ |
| config           | Configuration file                                           | No       | -                              |
| model_path       | Path of pre training weight                                  | Yes      | 配置文件中指定的预训练权重路径 |
| save_dir         | Path to save forecast model                                  | Yes      | output                         |
| input_shape      | Set the input shape of the exported model, such as input ` --input_shape 1 3 1024 1024`. If input_ shape is not set, by default, the input_shape of the exported model is [-1, 3, -1, -1] | Yes      | None                           |
| with_softmax     | Add softmax op at the end of the network. Since PaddleSeg networking returns logits by default, it can be set to True if you want to obtain the probability value of the deployment model | Yes      | False                          |
| without_argmax   | Whether the argmax op is not added at the end of the network. Since PaddleSeg networking returns logits by default, in order to obtain the prediction results directly from the deployment model, we add argmax operator at the end of the network by default | Yes      | False                          |

## 3. Static model

The following is the exported forecast model file.

```shell
output
  ├── deploy.yaml            # Deployment related configuration files mainly describe the data preprocessing method
  ├── model.pdmodel          # Topology file of static model
  ├── model.pdiparams        # Weight file of static model
  └── model.pdiparams.info   # Parameter additional information, generally no need to pay attention to
```