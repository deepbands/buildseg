import cv2
import numpy as np
import paddle.inference as paddle_infer


class InferWorker(object):
    def __init__(self, model_file, params_path, size=512):
        super(InferWorker, self).__init__()
        if model_file is not None and params_path is not None:
            config = paddle_infer.Config(model_file, params_path)  # Create config
            config.enable_use_gpu(200, 0)
            self.predictor = paddle_infer.create_predictor(config)  # Create predictor from config
        self.size = (size, size) if isinstance(size, int) else size
        _mean=[0.5] * 3
        _std=[0.5] * 3
        self._mean = np.float32(np.array(_mean).reshape(-1, 1, 1))
        self._std = np.float32(np.array(_std).reshape(-1, 1, 1))

    def load_model(self, model_file, params_path):
        config = paddle_infer.Config(model_file, params_path)
        config.enable_use_gpu(200, 0)
        self.predictor = paddle_infer.create_predictor(config)

    def _preprocess(self, img):
        img = cv2.resize(img, self.size, interpolation=cv2.INTER_CUBIC)
        img = (img.astype("float32") / 255.).transpose((2, 0, 1))
        img = (img - self._mean) / self._std
        C, H, W = img.shape
        img = img.reshape([1, C, H, W])
        return img

    def infer(self, img):
        # Get name of input
        input_names = self.predictor.get_input_names()
        input_handle = self.predictor.get_input_handle(input_names[0])
        # Set input
        input = self._preprocess(img)
        input_handle.reshape([1, 3, self.size[0], self.size[1]])
        input_handle.copy_from_cpu(input)
        # Run predictor
        self.predictor.run()
        # Get output
        output_names = self.predictor.get_output_names()
        output_handle = self.predictor.get_output_handle(output_names[0])
        output_data = output_handle.copy_to_cpu()  # Convert ndarray
        return np.squeeze(output_data.astype("uint8") * 255)


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