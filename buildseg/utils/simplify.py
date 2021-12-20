import os
import os.path as osp
from qgis import processing

try:
    from osgeo import gdal
except ImportError:
    import gdal


def simplify_polygon(infile, outfile, threshold=0.2):
    if osp.exists(outfile):
        os.remove(outfile)
    processing.run("native:simplifygeometries", \
        {'INPUT':infile, \
        'METHOD':0, \
        'TOLERANCE':threshold, \
        'OUTPUT':outfile})


def dowm_sample(file_path, scale=0.5):
    if scale == 1.0:
        return file_path
    path, named = osp.split(file_path)
    name, ext = osp.splitext(named)
    down_sample_save = osp.join(path, (name + "_down_sample" + ext))
    dataset = gdal.Open(file_path)
    band_count = dataset.RasterCount
    cols = dataset.RasterXSize
    rows = dataset.RasterYSize
    if scale < 0 and scale > 1:
        raise (f"scale must in [0, 1], now it is {scale}")
    else:
        scale = float(scale)
    # new cols and rows
    cols = int(cols * scale)
    rows = int(rows * scale)
    geotrans = list(dataset.GetGeoTransform())
    geotrans[1] = geotrans[1] / scale
    geotrans[5] = geotrans[5] / scale
    if osp.exists(down_sample_save):
        os.remove(down_sample_save)
    data_type = dataset.GetRasterBand(1).DataType
    target = dataset.GetDriver().Create(down_sample_save, xsize=cols, ysize=rows, \
                                        bands=band_count, eType=data_type)
    target.SetProjection(dataset.GetProjection())
    target.SetGeoTransform(geotrans)
    total = band_count + 1
    for index in range(1, total):
        data = dataset.GetRasterBand(index).ReadAsArray(buf_xsize=cols, buf_ysize=rows)
        out_band = target.GetRasterBand(index)
        out_band.SetNoDataValue(dataset.GetRasterBand(index).GetNoDataValue())
        out_band.WriteArray(data)
        out_band.FlushCache()
        out_band.ComputeBandStats(False)
    print("finished!")
    del dataset
    del target
    return down_sample_save


if __name__ == "__main__":
    # # test_1
    # infile = r"C:\Users\Geoyee\Desktop\dd\shp.shp"
    # outfile = r"C:\Users\Geoyee\Desktop\dd\shp_simp.shp"
    # simplify_polygon(infile, outfile)
    # test_2
    ras_path = r"E:\dataFiles\github\buildseg\data\test.tif"
    dowm_sample(ras_path, 0.5)