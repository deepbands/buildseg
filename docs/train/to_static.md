# Convert to static graph model

After training in AI Studio or local, we can get a parameter file of dynamic graph from the saved folder, which is ` *.pdparams`. But if it needs to be used in buildseg, we need to convert it into a static graph model.

## Files preparation

```shell
output
  ├── ocrnet_hrnet_w18_512x512.yml   # Network and preprocessing profile
  └── best_model.pdparams            # Dynamic graph parameters
```

The config file can be written into a YML file according to the parameters during network definition, which corresponds to the following :

- Python code about network :

  ```python
  model = OCRNet(num_classes=2,
                 backbone=HRNet_W18(),
                 backbone_indices=[0])
  ```

- Code in YML config :

  ```yaml
  model:
    num_classes: 2
    type: OCRNet
    backbone:
      type: HRNet_W18
    backbone_indices: [0]
  ```

The currently available config file is located in trained/to_ static folder.

## Convert

Executing the following command in the PaddleSeg's directory after ensuring that PaddleSeg is installed correctly, and the prediction model will be saved in the output folder.

```shell
# Set an available GPU
# export CUDA_VISIBLE_DEVICES=0  # linux / macos
set CUDA_VISIBLE_DEVICES=0  # windows

# export static graph model
python export.py \
       --config ocrnet_hrnet_w18_512x512.yml \
       --model_path model.pdparams \
       --save_dir output
```

### Parameter description

| Parameter's name | Purpose                                                      | Optional | Default                                          |
| ---------------- | ------------------------------------------------------------ | -------- | ------------------------------------------------ |
| config           | Path of config file                                          | No       | -                                                |
| model_path       | Path of dynamic graph model's parameter file                 | Yes      | Pre-training weight path specified in the config |
| save_dir         | Path of folder where the static graph model is saved         | Yes      | output                                           |
| input_shape      | Set the input shape of the exported model, such as input ` --input_shape 1 3 1024 1024`. If input_ shape is not set, by default, the input_shape of the exported model is [-1, 3, -1, -1] | Yes      | None                                             |
| with_softmax     | Add softmax op at the end of the network. Since PaddleSeg networking returns logits by default, it can be set to True if you want to obtain the probability value of the model | Yes      | False                                            |
| without_argmax   | Whether the argmax op is not added at the end of the network. Since PaddleSeg networking returns logits by default, in order to obtain the prediction results directly from the model, we add argmax op at the end of the network by default | Yes      | False                                            |

## 3. Static model

The following is the exported static graph model file.

```shell
output
  ├── deploy.yaml            # Deployment related configuration files mainly describe the data preprocessing method
  ├── model.pdmodel          # Topology file of static model
  ├── model.pdiparams        # Weight file of static model
  └── model.pdiparams.info   # Parameter additional information, generally no need to pay attention to
```