# -*- coding: utf-8 -*-
"""
/***************************************************************************
 buildSeg
                                 A QGIS plugin
 Deep learning building segmentation
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-11-01
        git sha              : $Format:%H$
        copyright            : (C) 2021 by geoyee
        email                : geoyee@yeah.net
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .buildSeg_dialog import buildSegDialog
# from qgis.utils import iface
from qgis.core import (
    QgsMapLayerProxyModel, QgsVectorFileWriter, QgsProject, Qgis)
from qgis.utils import iface

import os.path as osp
import time
import buildseg.utils as utils

try:
    from osgeo import gdal
except ImportError:
    import gdal
    
# # DEBUG
# import cv2


class buildSeg:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = osp.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        locale_path = osp.join(
            self.plugin_dir,
            "i18n",
            "buildSeg_{}.qm".format(locale))

        if osp.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u"&buildSeg")

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None
        self.gui_number = 0  # open one GUI
        self.check_pass = None  # check ones
        self.onnx_file = None
        self.infer_worker = None
        self.save_shp_path = None

        # Init block and overlap size
        self.block_size_list = [512]
        self.overlap_size_list = [(2 ** i) for i in range(9)]
        self.scale_list = [(i / 10) for i in range(10, 0, -1)]

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate("buildSeg", message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ":/plugins/buildSeg/icon.png"
        self.add_action(
            icon_path,
            text=self.tr(u"buildseg"),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True
        self.check_pass = False
        # initialization
        self.infer_worker = None


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u"&buildSeg"),
                action)
            self.iface.removeToolBarIcon(action)

    
    def mes_show(self, str, time, mode="info"):
        if mode == "info":
            iface.messageBar().pushMessage(str, level=Qgis.Info, duration=time)
        else:  # mode == "error"
            iface.messageBar().pushMessage(str, level=Qgis.Critical, duration=time)


    # Load parameters
    def select_onnx_file(self):
        self.onnx_file = self.dlg.mQfwParams.filePath()
        if osp.exists(self.onnx_file):
            if self.infer_worker is not None:
                self.infer_worker.load_model(self.onnx_file)
                self.mes_show("Parameters loaded successfully!", 5)
        else:
            self.onnx_file = None
            self.mes_show(f"Parameters loaded unsuccessfully, not find {self.onnx_file}.", 5)

    
    # Select shapefile save path
    def select_shp_save(self):
        self.save_shp_path = self.dlg.mQfwShape.filePath()


    # Simplify chackbox state
    def simp_state_change(self, state):
        self.dlg.lblThreshold.setEnabled(bool(state // 2))
        self.dlg.mQgsDoubleSpinBox.setEnabled(bool(state // 2))


    def init_setting(self):
        # Add setting
        self.dlg.mQfwParams.setFilter("*.onnx")
        self.dlg.mQfwShape.setFilter("*.shp")
        self.dlg.mMapLayerComboBoxR.setFilters(QgsMapLayerProxyModel.RasterLayer)
        # Add event
        self.dlg.mQfwParams.fileChanged.connect(self.select_onnx_file)  # load params
        self.dlg.mQfwShape.fileChanged.connect(self.select_shp_save)
        self.dlg.ccbSimplify.stateChanged.connect(self.simp_state_change)
        # show the dialog
        self.dlg.show()
        self.dlg.cbxBlock.addItems([str(s) for s in self.block_size_list])
        self.dlg.cbxOverlap.addItems([str(s) for s in self.overlap_size_list])
        self.dlg.cbxOverlap.setCurrentIndex(4)  # default 32
        self.dlg.cbxScale.addItems([str(s) for s in self.scale_list])
        # # quick test in my computer
        # self.dlg.cbxScale.setCurrentIndex(5)
        # self.dlg.mQfwShape.setFilePath(r"C:\Users\Geoyee\Desktop\dd\test.shp")
        # self.dlg.mQfwParams.setFilePath(
        #     r"E:\dataFiles\github\buildseg\static_weight\bisenet_v2_512x512\model.pdiparams")


    def run(self):
        """Run method that performs all the real work"""
        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        self.gui_number += 1
        if self.first_start == True:
            self.first_start = False
            self.dlg = buildSegDialog()
            self.init_setting()  # init all of widget's settings
        if self.gui_number == 1:  # avoid multiple startup plugin errors
            self.infer_worker = utils.InferWorker(self.onnx_file)
            # Run the dialog event loop
            result = self.dlg.exec_()
            # See if OK was pressed
            if result:
                if self.save_shp_path is not None and self.onnx_file is not None:
                    # Start timing
                    time_start = time.time()
                    # Get parameters
                    grid_size = [int(self.dlg.cbxBlock.currentText())] * 2
                    overlap = [int(self.dlg.cbxOverlap.currentText())] * 2
                    scale_rate = float(self.dlg.cbxScale.currentText())
                    print(f"grid_size is {grid_size}, overlap is {overlap}, " + \
                        "scale_rate is {scale_rate}.")
                    # layers = iface.activeLayer()  # Get the currently active layer
                    # Get the selected raster layer
                    current_raster_layer = self.dlg.mMapLayerComboBoxR.currentLayer()
                    # Band used by the current renderer
                    band_list = current_raster_layer.renderer().usesBands()
                    # Get the raster layer path
                    current_raster_layer_name = current_raster_layer.source()
                    # Add downsample
                    down_save_path = self.save_shp_path.replace(".shp", "_dowm.tif")
                    layer_path = utils.dowm_sample(current_raster_layer_name, \
                                                down_save_path, scale_rate)
                    print(f"layer_path: {layer_path}")
                    ras_ds = gdal.Open(layer_path)
                    geot = ras_ds.GetGeoTransform()
                    proj = ras_ds.GetProjection()
                    # If this layer is a raster layer
                    xsize = ras_ds.RasterXSize
                    ysize = ras_ds.RasterYSize
                    ras_ds = None
                    grid_count = utils.create_grids(ysize, xsize, grid_size, overlap)
                    number = grid_count[0] * grid_count[1]
                    # print(f"xsize is {xsize}, ysize is {ysize}, grid_count is {grid_count}")
                    print("Start block processing.")
                    geoinfo = {"row": ysize, "col": xsize, "geot": geot, "proj": proj}
                    mask_save_path = self.save_shp_path.replace(".shp", "_mask.tif")
                    mask = utils.Mask(mask_save_path, geoinfo, grid_size, overlap)
                    for i in range(grid_count[0]):
                        for j in range(grid_count[1]):
                            img = utils.layer2array(layer_path, band_list, \
                                                    i, j, grid_size, overlap)
                            # mask_grids[i][j] = self.infer_worker.infer(img, True)
                            mask.write_grid(self.infer_worker.infer(img, True), i, j)
                            print(f"-- {i * grid_count[1] + j + 1}/{number} --.")
                    # self.mes_show("Start Spliting.", 5)
                    # mask = utils.splicing_grids(mask_grids, ysize, xsize, grid_size, overlap)
                    print("Start generating result file.")
                    # raster to shapefile used GDAL
                    is_simp = self.dlg.ccbSimplify.isChecked()
                    utils.polygonize_raster(mask, self.save_shp_path, proj, geot, \
                                            display=(not is_simp))
                    if is_simp is True:
                        simp_save_path = self.save_shp_path.replace(".shp", "_simp.shp")
                        utils.simplify_polygon(self.save_shp_path, simp_save_path, \
                                            self.dlg.mQgsDoubleSpinBox.value())
                        iface.addVectorLayer(simp_save_path, "deepbands-simplified", "ogr")
                    time_end = time.time()
                    self.mes_show(
                        ("The whole operation is performed in {0} seconds.".format(
                            str(time_end - time_start))), 30)
                else:
                    self.mes_show("params_file is None.", 10, "error")
        else:
            self.mes_show("The GUI of the plugin has been displayed.", 5)
        self.gui_number -= 1