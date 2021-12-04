import numpy as np
from .raster2uint8 import raster_to_uint8

try:
    import gdal
except:
    from osgeo import gdal


# def raster2ndarray(lyr):
#     '''
#         input: lyr(QgsMapLayerType.QgsRasterLayer)
#         output: _(ndarray)
#     '''
#     provider= lyr.dataProvider()
#     # Band number
#     blocks = []
#     for c in range(lyr.bandCount()):
#         blocks.append(provider.block((c + 1), lyr.extent(), lyr.width(), lyr.height()))
#     values=[]
#     for i in range(lyr.width()):
#         tmps = []
#         for j in range(lyr.height()):
#             tmps.append([blocks[k].value(i, j) for k in range(lyr.bandCount())])
#         values.append(tmps)
#     return np.array(values)


def layer2array(layer, row=None, col=None, grid_size=[512, 512], overlap=[24, 24]):
    gd = gdal.Open(str(layer.source()))
    band_list = layer.renderer().usesBands()  # Band used by the current renderer
    width, height = layer.width(), layer.height()
    if gd.RasterCount != 1:
        array_list = []
        for b in band_list:
            band = gd.GetRasterBand(b)
            array_list.append(raster_to_uint8(get_grid(band, row, col, \
                                                       width, height, grid_size, overlap)))
        array = np.stack(array_list, axis=2)
    else:
        array = raster_to_uint8(get_grid(gd, row, col, \
                                         width, height, grid_size, overlap))
    return array


def get_grid(gd, row, col, width, height, grid_size, overlap):
    grid_size = np.array(grid_size)
    overlap = np.array(overlap)
    if row is not None and col is not None:
        grid_idx = np.array([row, col])
        ul = grid_idx * (grid_size - overlap)
        lr = ul + grid_size
        # print("ul, lr", ul, lr)
        xoff, yoff, xsize, ysize = ul[1], ul[0], (lr[1] - ul[1]), (lr[0] - ul[0])
        if xoff + xsize > width:
            xsize = width - xoff
        if yoff + ysize > height:
            ysize = height - yoff
        result = gd.ReadAsArray(xoff=int(xoff), yoff=int(yoff), \
                                win_xsize=int(xsize), win_ysize=int(ysize))
    else:
        result = gd.ReadAsArray()
    return result


def convert_coord(point, tform):
    olp = np.ones((1, 3))
    olp[0, :2] = point
    nwp = np.dot(tform, olp.T)
    return nwp.T[0, :2]