import cv2
import numpy as np
from .postpro import *
import paddle.inference as paddle_infer


class InferWorker(object):
    def __init__(self, model_file, params_path, size=512, use_gpu=True):
        super(InferWorker, self).__init__()
        if model_file is not None and params_path is not None:
            self.load_model(model_file, params_path, use_gpu)
        self.size = (size, size) if isinstance(size, int) else size
        _mean=[0.5] * 3
        _std=[0.5] * 3
        self._mean = np.float32(np.array(_mean).reshape(-1, 1, 1))
        self._std = np.float32(np.array(_std).reshape(-1, 1, 1))

    def load_model(self, model_file, params_path, use_gpu=True):
        config = paddle_infer.Config(model_file, params_path)  # Create config
        if not use_gpu:
            config.enable_mkldnn()
            config.enable_mkldnn_bfloat16()
            config.switch_ir_optim(True)
            config.set_cpu_math_library_num_threads(10)
        else:
            config.enable_use_gpu(500, 0)
            config.switch_ir_optim()
            config.enable_memory_optim()
            config.enable_tensorrt_engine(
                workspace_size=1 << 30,
                precision_mode=paddle_infer.PrecisionType.Float32,
                max_batch_size=1,
                min_subgraph_size=5,
                use_static=False,
                use_calib_mode=False
            )
        self.predictor = paddle_infer.create_predictor(config)  # Create predictor from config

    def reset_model(self):
        self.predictor = None

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
        # Get name of input
        input_names = self.predictor.get_input_names()
        input_handle = self.predictor.get_input_handle(input_names[0])
        # Set input
        input = self.__preprocess(img)
        input_handle.reshape([1, 3, self.size[0], self.size[1]])
        input_handle.copy_from_cpu(input)
        # Run predictor
        self.predictor.run()
        # Get output
        output_names = self.predictor.get_output_names()
        output_handle = self.predictor.get_output_handle(output_names[0])
        output_data = output_handle.copy_to_cpu()  # Convert ndarray
        result = np.squeeze(output_data.astype("uint8"))
        result = self.__postprocess(result)
        if mul_255 is True:
           result *= 255
        return result


# test
if __name__ == "__main__":
    img_path = "train/dataset/img/4_1_bc.jpg"
    model_path = "static_weight/model.pdmodel"
    params_path = "static_weight/model.pdiparams"
    infer_worker = InferWorker(model_path, params_path)
    img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)
    pred = infer_worker.infer(img)
    print(type(pred), pred.shape)
    cv2.imshow("test", pred)
    cv2.waitKey(0)
    cv2.destroyAllWindows()