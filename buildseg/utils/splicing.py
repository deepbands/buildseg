import numpy as np

try:
    from osgeo import gdal
except ImportError:
    import gdal


def create_grids(ysize, xsize, grid_size=[512, 512], overlap=[24, 24]):
    img_size = np.array([ysize, xsize])
    grid_size = np.array(grid_size)
    overlap = np.array(overlap)
    grid_count = np.ceil(img_size / (grid_size - overlap))
    grid_count = grid_count.astype("uint16")
    # mask_grids = [[np.zeros(grid_size) \
    #                for _ in range(grid_count[1])] for _ in range(grid_count[0])]
    # return list(grid_count), mask_grids
    return list(grid_count)


# def splicing_grids(img_list, ysize, xsize, grid_size=[512, 512], overlap=[24, 24]):
#     raw_size = np.array([ysize, xsize])
#     grid_size = np.array(grid_size)
#     overlap = np.array(overlap)
#     h, w = grid_size
#     # row = math.ceil(raw_size[0] / h)
#     # col = math.ceil(raw_size[1] / w)
#     row, col = len(img_list), len(img_list[0])
#     # print("row, col:", row, col)
#     result_1 = np.zeros((h * row, w * col), dtype=np.uint8)
#     result_2 = result_1.copy()
#     for i in range(row):
#         for j in range(col):
#             # print("h, w:", h, w)
#             ih, iw = img_list[i][j].shape[:2]
#             im = np.zeros(grid_size)
#             im[:ih, :iw] = img_list[i][j]
#             start_h = (i * h) if i == 0 else (i * (h - overlap[0]))
#             end_h = start_h + h
#             start_w = (j * w) if j == 0 else (j * (w - overlap[1]))
#             end_w = start_w + w
#             # print("se: ", start_h, end_h, start_w, end_w)
#             # Or operation on overlapping areas
#             if (i + j) % 2 == 0:
#                 result_1[start_h: end_h, start_w: end_w] = im
#             else:
#                 result_2[start_h: end_h, start_w: end_w] = im
#             # print("r, c, k:", i_r, i_c, k)
#     result = np.where(result_2 != 0, result_2, result_1)
#     result = result[:raw_size[0], :raw_size[1]]
#     return result


class Mask(object):
    def __init__(self, file_name, geoinfo, grid_size=[512, 512], overlap=[24, 24]) -> None:
        self.file_name = file_name
        self.raw_size = np.array([geoinfo["row"], geoinfo["col"]])
        self.grid_size = np.array(grid_size)
        self.overlap = np.array(overlap)
        driver = gdal.GetDriverByName("GTiff")
        self.dst_ds = driver.Create(file_name, geoinfo["col"], geoinfo["row"], 1, gdal.GDT_UInt16)
        self.dst_ds.SetGeoTransform(geoinfo["geot"])
        self.dst_ds.SetProjection(geoinfo["proj"])
        self.band = self.dst_ds.GetRasterBand(1)
        self.band.WriteArray(np.zeros((self.raw_size[0], self.raw_size[1]), dtype="uint8"))

    def write_grid(self, grid, i, j):
        h, w = self.grid_size
        start_h = (i * h) if i == 0 else (i * (h - self.overlap[0]))
        end_h = start_h + h
        if end_h > self.raw_size[0]:
            win_ysize = int(self.raw_size[0] - start_h)
        else:
            win_ysize = int(self.grid_size[1])
        start_w = (j * w) if j == 0 else (j * (w - self.overlap[1]))
        end_w = start_w + w
        if end_w > self.raw_size[1]:
            win_xsize = int(self.raw_size[1] - start_w)
        else:
            win_xsize = int(self.grid_size[0])
        over_grid = self.band.ReadAsArray(xoff=int(start_w), yoff=int(start_h), \
                                          win_xsize=win_xsize, win_ysize=win_ysize)
        h, w = over_grid.shape
        # print(h, w)
        over_grid += grid[:h , :w]
        over_grid[over_grid > 0] = 1
        self.band.WriteArray(over_grid, int(start_w), int(start_h))
        self.dst_ds.FlushCache()

    @property
    def gdal_data(self):
        return self.dst_ds

    def close(self):
        self.dst_ds = None