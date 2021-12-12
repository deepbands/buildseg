import os

try:
    import gdal
    import ogr
    import osr
except:
    from osgeo import gdal, ogr, osr


def __mask2tif(mask, tmp_path, tf, proj):
    row, columns = mask.shape[:2]
    dim = 1
    driver = gdal.GetDriverByName("GTiff")
    dst_ds = driver.Create(tmp_path, columns, row, dim, gdal.GDT_UInt16)
    dst_ds.SetGeoTransform(tf)
    dst_ds.SetProjection(proj)
    dst_ds.GetRasterBand(1).WriteArray(mask)
    dst_ds.FlushCache()
    return dst_ds


# BUG: proj is error
def polygonize_raster(mask, shp_save_path, tf, crs, rm_tmp=True):
    tmp_path = shp_save_path.replace(".shp", ".tif")
    ds = __mask2tif(mask, tmp_path, tf, crs.toProj4())
    srcband = ds.GetRasterBand(1)
    maskband = srcband.GetMaskBand()
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    gdal.SetConfigOption("SHAPE_ENCODING", "UTF-8")
    ogr.RegisterAll()
    drv = ogr.GetDriverByName("ESRI Shapefile")
    dst_ds = drv.CreateDataSource(shp_save_path)
    prosrs = osr.SpatialReference()
    prosrs.ImportFromEPSG(crs.srsid())
    geosrs = prosrs.CloneGeogCS()
    dst_layer = dst_ds.CreateLayer("Building boundary", geosrs)
    dst_fieldname = "DN"
    fd = ogr.FieldDefn(dst_fieldname, ogr.OFTInteger)
    dst_layer.CreateField(fd)
    gdal.Polygonize(srcband, maskband, dst_layer, 0, [])
    dst_ds.Destroy()
    ds = None
    if rm_tmp:
        os.remove(tmp_path)


if __name__ == "__main__":
    # import numpy as np
    # img = np.eye(256, 256, dtype="uint8")
    # ds = __mask2tif(img, (2037.0, 10.0, 0.0, 11238.000000000002, 0.0, -10.0))
    # print(type(ds))
    # srcband = ds.GetRasterBand(1)
    # print(type(srcband))
    # maskband = srcband.GetMaskBand()
    # print(type(maskband))
    prosrs = osr.SpatialReference()
    prosrs.ImportFromEPSG(32737)
    print(prosrs)
    prosrs.ImportFromProj4("+proj=utm +zone=37 +south +datum=WGS84 +units=m +no_defs")
    print(prosrs)