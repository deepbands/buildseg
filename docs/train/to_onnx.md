# Convert to ONNX model

After training in AI Studio or local, we can get a parameter file of dynamic graph from the saved folder, which is ` *.pdparams`. But if it needs to be used in buildseg, we need to convert it into a ONNX model.

## Preparation

Prepare the dynamic graph model (` *.Pdparams `) and install the third-party dependency library:

```shell
cd scripts
pip install -r requirements.txt
```

## Convert

Executing the following command:

```shell
python to_onnx.py \
       --model_name model \
       --params_path model.pdparams
```

#### Parameter description

| Parameter's name |                       Purpose                        | Optional |    Default     |            Values            |
| :--------------: | :--------------------------------------------------: | :------: | :------------: | :--------------------------: |
|    model_name    |                    Name of model                     |    No    |       -        | ocrnet / segformer / bisenet |
|   params_path    |     Path of dynamic graph model's parameter file     |    No    |       -        |              -               |
|    save_path     | Path of folder where the static graph model is saved |   Yes    | ../onnx_weight |              -               |

### Check model

Executing the following command:

```shell
python check_onnx.py
```

#### Parameter description

| Parameter's name |                       Purpose                        | Optional |    Default     |
| :--------------: | :--------------------------------------------------: | :------: | :------------: |
|    save_path     | Path of folder where the static graph model is saved |   Yes    | ../onnx_weight |
