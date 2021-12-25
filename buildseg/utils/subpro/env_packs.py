import cv2
import numpy as np
import paddle


if __name__ == "__main__":
    packages = {
        "paddle": paddle.__version__,
        "opencv": cv2.__version__,
        "numpy": np.__version__
    }
    print(packages)