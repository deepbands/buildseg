import numpy as np
import math


def create_grids(ysize, xsize, grid_size=[512, 512], overlap=[24, 24]):
    img_size = np.array([ysize, xsize])
    grid_size = np.array(grid_size)
    overlap = np.array(overlap)
    remainder = np.mod(img_size, grid_size)  # Mod
    grid_count = np.ceil((img_size + overlap) / grid_size)
    for i in range(2):
        if remainder[i] > overlap[i]:
            grid_count[i] += 1
    # grid_count = np.ceil((img_size + overlap) / grid_size)
    grid_count = grid_count.astype("uint16")
    mask_grids = [[np.zeros(grid_size) \
                   for _ in range(grid_count[1])] for _ in range(grid_count[0])]
    return list(grid_count), mask_grids


def splicing_grids(img_list, ysize, xsize, grid_size=[512, 512], overlap=[24, 24]):
    raw_size = np.array([ysize, xsize])
    grid_size = np.array(grid_size)
    overlap = np.array(overlap)
    h, w = grid_size
    # row = math.ceil(raw_size[0] / h)
    # col = math.ceil(raw_size[1] / w)
    row, col = len(img_list), len(img_list[0])
    # print("row, col:", row, col)
    result_1 = np.zeros((h * row, w * col), dtype=np.uint8)
    result_2 = result_1.copy()
    for i in range(row):
        for j in range(col):
            # print("h, w:", h, w)
            ih, iw = img_list[i][j].shape[:2]
            im = np.zeros(grid_size)
            im[:ih, :iw] = img_list[i][j]
            start_h = (i * h) if i == 0 else (i * (h - overlap[0]))
            end_h = start_h + h
            start_w = (j * w) if j == 0 else (j * (w - overlap[1]))
            end_w = start_w + w
            # print("se: ", start_h, end_h, start_w, end_w)
            # Or operation on overlapping areas
            if (i + j) % 2 == 0:
                result_1[start_h: end_h, start_w: end_w] = im
            else:
                result_2[start_h: end_h, start_w: end_w] = im
            # print("r, c, k:", i_r, i_c, k)
    result = np.where(result_2 != 0, result_2, result_1)
    result = result[:raw_size[0], :raw_size[1]]
    return result