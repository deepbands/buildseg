import os

try:
    from osgeo import gdal, ogr, osr
except ImportError:
    import gdal
    import ogr
    import osr


def __mask2tif(mask, tmp_path, proj, geot):
    row, columns = mask.shape[:2]
    dim = 1
    driver = gdal.GetDriverByName("GTiff")
    dst_ds = driver.Create(tmp_path, columns, row, dim, gdal.GDT_UInt16)
    dst_ds.SetGeoTransform(geot)
    dst_ds.SetProjection(proj)
    dst_ds.GetRasterBand(1).WriteArray(mask)
    dst_ds.FlushCache()
    return dst_ds


def polygonize_raster(mask, shp_save_path, proj, geot, rm_tmp=True):
    tmp_path = shp_save_path.replace(".shp", ".tif")
    ds = __mask2tif(mask, tmp_path, proj, geot)
    srcband = ds.GetRasterBand(1)
    maskband = srcband.GetMaskBand()
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    gdal.SetConfigOption("SHAPE_ENCODING", "UTF-8")
    ogr.RegisterAll()
    drv = ogr.GetDriverByName("ESRI Shapefile")
    dst_ds = drv.CreateDataSource(shp_save_path)
    prosrs = osr.SpatialReference(wkt=ds.GetProjection())
    ESPGValue = prosrs.GetAttrValue('AUTHORITY', 1)
    sr = osr.SpatialReference()
    sr.ImportFromEPSG(int(ESPGValue))
    dst_layer = dst_ds.CreateLayer("Building boundary", geom_type=ogr.wkbPolygon, srs=sr)
    dst_fieldname = "DN"
    fd = ogr.FieldDefn(dst_fieldname, ogr.OFTInteger)
    dst_layer.CreateField(fd)
    gdal.Polygonize(srcband, maskband, dst_layer, 0, [])
    dst_ds.Destroy()
    ds = None
    if rm_tmp:
        os.remove(tmp_path)