# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Layer_arranger
                                 A QGIS plugin
 This plugin is used to automatically group and arrange the layer in the way that is optimizes layer visibility.
                              -------------------
        begin                : 2014-12-10
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Abhijit Gujar
        email                : abhijitgujar86@gmail.com
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Import the code for the dialog
from layer_arranger_dialog import Layer_arrangerDialog
import os.path
from PyQt4.QtCore import QFileInfo
from qgis.core import *
from PyQt4.QtGui import *


class Layer_arranger:
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
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Layer_arranger_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = Layer_arrangerDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Layer arranger')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'Layer_arranger')
        self.toolbar.setObjectName(u'Layer_arranger')

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
        return QCoreApplication.translate('Layer_arranger', message)


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
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/Layer_arranger/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'layer arranger'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Layer arranger'),
                action)
            self.iface.removeToolBarIcon(action)


    def run(self):
        #make the desired groups for layers
        root = QgsProject.instance().layerTreeRoot()
        #x=root.findGroup("Group Point")
        #if x == "Group Point"
        #    QMessageBox.information( self.iface.mainWindow(),"Stop", "Group already exist .."
        toc = self.iface.legendInterface()
        layers = QgsMapLayerRegistry.instance().mapLayers()

        if root.findGroup("Group Point") is None:
            root.insertGroup(0, "Group Point")
            root.insertGroup(1, "Group Line")
            root.insertGroup(2, "Group Polygon")
            print 'helloooo 2'
            #get the list of layers  from registry
            #segregate layers into groups
            for name, layer in layers.iteritems():
                # check the layer geometry type
                if layer.geometryType() == QGis.Point:
                    toc.moveLayer(layer, 0)

                if layer.geometryType() == QGis.Line:
                    toc.moveLayer(layer, 1)

                if layer.geometryType() == QGis.Polygon:
                    toc.moveLayer(layer, 2)
        else:
            for name, layer in layers.iteritems():             # check the layer geometry type
                 # check the layer geometry type
                if layer.geometryType() == QGis.Point:
                    toc.moveLayer(layer, 0)

                if layer.geometryType() == QGis.Line:
                    toc.moveLayer(layer, 1)

                if layer.geometryType() == QGis.Polygon:
                    toc.moveLayer(layer, 2)
            #QMessageBox.information(self.iface.mainWindow(),"Layer Arranger", " Sorry: You can run the Layer Arranger only once and group Group Point, Group Line, Group Polygon should not be repeated.")
