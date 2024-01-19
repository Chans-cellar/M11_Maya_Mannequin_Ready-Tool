import typing

import maya.cmds as cmds

import os

from PySide2.QtCore import *
from PySide2.QtCore import Qt
from PySide2.QtWidgets import *
from PySide2.QtWidgets import QTreeWidgetItem
from PySide2.QtUiTools import QUiLoader
from maya import OpenMayaUI
from shiboken2 import wrapInstance
from PySide2.QtGui import QPixmap
import json

# from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.OpenMayaUI as omui

mayaMainWindowPtr = OpenMayaUI.MQtUtil.mainWindow()
mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)


class Manne_Hierachy(QWidget):

    def __init__(self, *args, **kwargs):
        super(Manne_Hierachy, self).__init__(*args, **kwargs)

        self.setObjectName('Manne_Hierachy')
        self.setWindowTitle('Mannequin Hierachy')
        self.setWindowFlags(Qt.Window)
        self.init_UI()
        self.RootName = None
        self.OriginalMeshHierarchy = True

    def init_UI(self):
        usd = cmds.internalVar(usd=True)
        UI_FILE = os.path.join(usd, 'Mannequin_Hierachy_v1', 'Resources', 'Manne_Hierachy.ui')
        ui_file = QFile(UI_FILE)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()

        self.ui = loader.load(ui_file, parentWidget=self)
        ui_file.close()

        self.rigName_Selector = self.ui.rigName_Selector
        self.layerHirachyWidget = self.ui.layerHirachyWidget
        self.ui.createHierachy_Button.clicked.connect(self.clean_Hierarchy)
        self.ui.revert_Button.clicked.connect(self.revert_deletion)
        self.load_RootRig()
        self.load_LayerHierachy('Geometry')

    def run_UI(self):
        self.ui.show()

    def load_RootRig(self):
        self.rigName_Selector.clear()
        roots = cmds.ls(assemblies=True)
        for item in roots:
            # get the objects that endswith rig keyword and add to the dropdown
            if item.endswith('Rig'):
                self.rigName_Selector.addItem(item)

    def load_LayerHierachy(self, geometryParentGroup):
        self.layerHirachyWidget.clear()
        # cmds.select(geometryParentGroup)
        self.layerHirachyWidget.setColumnCount(1)
        self.layerHirachyWidget.setHeaderLabel(geometryParentGroup)
        try:
            meshGroups = cmds.listRelatives(geometryParentGroup, c=True)

            for item in meshGroups:
                parent = QTreeWidgetItem(self.layerHirachyWidget, [item])
                meshes = cmds.listRelatives(item, c=True)
                for mesh in meshes:
                    child = QTreeWidgetItem(parent, [mesh])
                    child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                    child.setCheckState(0, Qt.Unchecked)
                    parent.addChild(child)
        except:
            print('No Geometry Object')

    # selected = []
    # for i in range(0, widget.count()):
    #     if widget.item(i).isChecked():
    #         selected.append(i)

    # get the checked meshes
    def clean_Hierarchy(self):
        _root = self.layerHirachyWidget.invisibleRootItem()
        meshGroups_count = _root.childCount()
        cmds.undoInfo(openChunk=True)

        for i in range(meshGroups_count):
            _meshGroup = _root.child(i)
            is_checked_meshGroup = False
            meshes_count = _meshGroup.childCount()

            for j in range(meshes_count):
                _mesh = _meshGroup.child(j)

                if _mesh.checkState(0) == Qt.Checked:
                    is_checked_meshGroup = True
                    # unChecked_meshes.append(_mesh.text(0))
                else:
                    cmds.delete(_mesh.text(0))

            if not is_checked_meshGroup:
                cmds.delete(_meshGroup.text(0))


    def revert_deletion(self):
        cmds.undoInfo(closeChunk=True)
        cmds.undo()
        self.load_LayerHierachy('Geometry')

    # delete the unchecked meshes
    # revoke back to the original


try:
    Manne_Hierachy.close()
    Manne_Hierachy.deleteLater()
except:
    pass
ManneHierachy = Manne_Hierachy()
ManneHierachy.run_UI()
