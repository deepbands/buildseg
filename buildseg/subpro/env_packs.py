try:
    import cv2
    opencv_ver = cv2.__version__
except ImportError:
    opencv_ver = None
try:
    import numpy as np
    numpy_ver = np.__version__
except ImportError:
    numpy_ver = None
try:
    import paddle
    paddle_ver = paddle.__version__
except ImportError:
    paddle_ver = None

packages = {
    "paddle": paddle_ver,
    "opencv": opencv_ver,
    "numpy": numpy_ver
}

print(packages)