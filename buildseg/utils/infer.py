import cv2
import numpy as np
import onnxruntime

try:
    from .postpro import *
except ImportError:
    from postpro import *  # for test


class InferWorker(object):
    def __init__(self, onnx_file, size=512):
        super(InferWorker, self).__init__()
        if onnx_file is not None:
            self.ort_sess = onnxruntime.InferenceSession(onnx_file)
        self.size = (size, size) if isinstance(size, int) else size
        _mean=[0.5] * 3
        _std=[0.5] * 3
        self._mean = np.float32(np.array(_mean).reshape(-1, 1, 1))
        self._std = np.float32(np.array(_std).reshape(-1, 1, 1))

    def load_model(self, onnx_file):
        self.ort_sess = onnxruntime.InferenceSession(onnx_file)

    def __preprocess(self, img):
        h, w = img.shape[:2]
        tmp = np.zeros((self.size[0], self.size[1], 3), dtype="uint8")
        tmp[:h, :w, :] = img
        img = cv2.resize(tmp, self.size, interpolation=cv2.INTER_CUBIC)
        img = (img.astype("float32") / 255.).transpose((2, 0, 1))
        img = (img - self._mean) / self._std
        C, H, W = img.shape
        img = img.reshape([1, C, H, W])
        return img

    def __postprocess(self, img):
        # 1. Open / Close operation: noise removal / hole filling
        img = open_and_close_op(img)
        # 2. Delete small connected area
        img = del_samll_area(img)
        # 3. Boundary smoothing
        img = bound_smooth(img)
        return img

    def infer(self, img, mul_255=True):
        x = self.__preprocess(img)
        ort_inputs = {self.ort_sess.get_inputs()[0].name: x}
        ort_outs = self.ort_sess.run(None, ort_inputs)
        result = np.squeeze(np.argmax(ort_outs[0], axis=1).astype("uint8"))
        result = self.__postprocess(result)
        if mul_255 is True:
           result *= 255
        return result


# test
if __name__ == "__main__":
    img_path = "data/train.jpg"
    onnx_file = "onnx_weight/bisenet_v2_512x512_rs_building.onnx"
    infer_worker = InferWorker(onnx_file)
    img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)
    pred = infer_worker.infer(img)
    print(type(pred), pred.shape)
    cv2.imshow("test", pred)
    cv2.waitKey(0)
    cv2.destroyAllWindows()