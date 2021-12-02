import numpy as np

try:
    import gdal
except:
    from osgeo import gdal


# TODO: 效率低
def raster2ndarray(lyr):
    '''
        input: lyr(QgsMapLayerType.QgsRasterLayer)
        output: _(ndarray)
    '''
    provider= lyr.dataProvider()
    # 多少个波段
    blocks = []
    for c in range(lyr.bandCount()):
        blocks.append(provider.block((c + 1), lyr.extent(), lyr.width(), lyr.height()))
    values=[]
    for i in range(lyr.width()):
        tmps = []
        for j in range(lyr.height()):
            tmps.append([blocks[k].value(i, j) for k in range(lyr.bandCount())])
        values.append(tmps)
    return np.array(values)


# TODO: 会不会更加占用内存，目前最好的解决方案
def layer2array(layer):
    gd = gdal.Open(str(layer.source()))
    band_list = layer.renderer().usesBands()  # 当前渲染器使用的波段
    if gd.RasterCount != 1:
        array_list = []
        for b in band_list:
            band = gd.GetBand(b)
            array_list.append(band.ReadAsArray())
        array = np.stack(array_list, axis=2)
    else:
        array = gd.ReadAsArray()
    return array


def convert_coord(point, tform):
    olp = np.ones((1, 3))
    olp[0, :2] = point
    nwp = np.dot(tform, olp.T)
    return nwp.T[0, :2]