# 转换为ONNX模型

当我们使用AI Studio或者本地训练好之后，就可以从保存的文件夹得到动态图的参数文件，为`*.pdparams`。我们需要将其转变为ONNX模型后，才能被buildseg所使用的。

## 准备

准备好动态图模型（`*.pdparams`），并安装第三方依赖库：

```shell
cd scripts
pip install -r requirements.txt
```

## 转换

执行如下命令：

```shell
python to_onnx.py \
       --model_name model \
       --params_path model.pdparams
```

#### 参数解释

|   参数名    |        用途        | 是否必选项 |     默认值     |             值表             |
| :---------: | :----------------: | :--------: | :------------: | :--------------------------: |
| model_name  |      模型名称      |     是     |       -        | ocrnet / segformer / bisenet |
| params_path |  预训练权重的路径  |     是     |       -        |              -               |
|  save_path  | 保存预测模型的路径 |     否     | ../onnx_weight |              -               |

### 检测模型

执行如下命令：

```shell
python check_onnx.py
```

#### 参数解释

|  参数名   |        用途        | 是否必选项 |     默认值     |
| :-------: | :----------------: | :--------: | :------------: |
| save_path | 保存预测模型的路径 |     否     | ../onnx_weight |
