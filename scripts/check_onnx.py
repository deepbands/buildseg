import os
import os.path as osp
import onnx
import argparse


parser = argparse.ArgumentParser(description="input parameters")
parser.add_argument("--save_path", type=str, default="../onnx_weight")


if __name__ == "__main__":
    save_path = parser.parse_args().save_path
    onnx_files_name = os.listdir(save_path)
    for name in onnx_files_name:
        onnx_file = osp.join(save_path, name)
        onnx_model = onnx.load(onnx_file)
        onnx.checker.check_model(onnx_model)
        print("[Checked] " + name.split(".")[0])