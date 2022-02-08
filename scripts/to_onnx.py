import os
import os.path as osp
import paddle
from paddleseg.models import OCRNet, HRNet_W18
from paddleseg.models.segformer import SegFormer_B2
from paddleseg.models import BiSeNetV2
import argparse


def dynamic2onnx(model, save_path):
    model.eval()
    x_spec = paddle.static.InputSpec([None, 3, 512, 512], "float32", "x")
    paddle.onnx.export(model, save_path, input_spec=[x_spec], opset_version=11)


parser = argparse.ArgumentParser(description="input parameters")
parser.add_argument("--model_name", type=str, required=True, help="ocrnet/segformer/bisenet")
parser.add_argument("--params_path", type=str, required=True)
parser.add_argument("--save_path", type=str, default="../onnx_weight")


if __name__ == "__main__":
    args = parser.parse_args()
    if args.model_name == "ocrnet":
        model = OCRNet(num_classes=2,
                       backbone=HRNet_W18(),
                       backbone_indices=[0])
    elif args.model_name == "segformer":
        model = SegFormer_B2(num_classes=2)
    elif args.model_name == "bisenet":
        model = BiSeNetV2(num_classes=2)
    model.set_state_dict(paddle.load(args.params_path))
    name = osp.splitext(osp.split(args.params_path)[-1])[0]
    dynamic2onnx(model, osp.join(args.save_path, name))