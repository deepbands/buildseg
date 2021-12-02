import os.path as osp
import numpy as np
import cv2
import paddle
from paddleseg.models.unet import UNet


class InferWorker:
    MODELS = {"unet": UNet(num_classes=2)}
    
    def __init__(self, model: str, params_path=None, size_tuple=(256, 256)) -> None:
        self.seg_model = self.MODELS[model]
        if params_path is not None:
            self.load_params(params_path)
        self.params_path = params_path
        self.size_tuple = size_tuple
        __mean=[0.5] * 3
        __std=[0.5] * 3
        self.__mean = np.float32(np.array(__mean).reshape(-1, 1, 1))
        self.__std = np.float32(np.array(__std).reshape(-1, 1, 1))

    def load_params(self, path):
        if osp.exists(path):
            params = paddle.load(path)
            self.seg_model.set_state_dict(params)
            self.params_path = path
            print("加载参数成功")
        else:
            print("未找到参数路径")

    def __process(self, img):
        img = cv2.resize(img, self.size_tuple, interpolation=cv2.INTER_CUBIC)
        img = (img.astype("float32") / 255.).transpose((2, 0, 1))
        img = (img - self.__mean) / self.__std
        C, H, W = img.shape
        img = img.reshape([1, C, H, W])
        return paddle.to_tensor(img)

    def __tensor2result(self, pre):
        if isinstance(pre, list):
            pre = pre[0]
        pred = paddle.argmax(pre, axis=1).numpy()
        # 标注反了
        pred -= 1
        pred *= -255
        return pred.astype("uint8").squeeze()

    def get_mask(self, img):
        img = self.__process(img)
        pre = self.seg_model(img)
        pred = self.__tensor2result(pre)
        return pred