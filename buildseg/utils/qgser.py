import numpy as np
from qgis.utils import iface
from qgis.core import QgsProject, QgsVectorLayer, QgsGeometry, QgsFeature
from .convert import convert_coord


def __getgtypes():
    return 'point', 'linestring', 'polygon', \
           'multipoint', 'multilinestring', 'multipolygon'


def showgeoms(geoms, name="tmp", gtype=None, proj=None):
    if gtype is None:
        gtype = geoms[0].constGet().geometryType() \
                if isinstance(geoms[0], QgsGeometry) else geoms[0].geometryType()
        gtype = gtype.lower()
    if gtype not in __getgtypes():
        raise Exception("gtype should be one of :{" + ','.join(__getgtypes()) + "}")
    vl = QgsVectorLayer(gtype, name, "memory")
    pr = vl.dataProvider()
    feats = []
    for geom in geoms:
        feat = QgsFeature()
        feat.setGeometry(geom)
        feats.append(feat)
    pr.addFeatures(feats)
    if proj is not None:
        vl.setCrs(proj)
    QgsProject.instance().addMapLayer(vl)
    iface.zoomFull()


def get_transform(result, size_tuple):
    extent_result = result.extent()
    # n_cols = result.width()
    # n_rows = result.height()
    n_rows, n_cols = size_tuple
    tform = np.array([[extent_result.width() / n_cols, 0.0, extent_result.xMinimum()],
		     [0.0, -extent_result.height() / n_rows, extent_result.yMaximum()],
             [0, 0, 1]])
    return tform


def __bound2wkt(bound_points, tform):
    wkts_str = "MultiPolygon ("
    for bps in bound_points:
        wbk = "(("
        for i in range(len(bps)):
            x, y = convert_coord(bps[i], tform)
            wbk += (str(x) + " " + str(y)) + ","
        x, y = convert_coord(bps[0], tform)
        wbk += (str(x) + " " + str(y)) + ")),"
        wkts_str += wbk
    wkts_str = wkts_str[:-1] + ")"
    return wkts_str


def bound2shp(bound_points, tform):
    wkt = __bound2wkt(bound_points, tform)
    polygon = QgsGeometry.fromWkt(wkt)
    return polygon