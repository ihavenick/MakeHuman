#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

import log
import gui
from export import Exporter
from exportutils.config import Config


class MhxConfig(Config):

    def __init__(self, exporter):
        from armature.options import ArmatureOptions
        from .mhx_rigify import RigifyOptions

        Config.__init__(self)
        self.useTexFolder =         exporter.useTexFolder.selected
        self.scale,self.unit =      exporter.taskview.getScale()
        self.useRelPaths =          True
        self.helpers =              True

        self.feetOnGround =         exporter.feetOnGround.selected
        self.useMasks =             True # exporter.masks.selected
        self.expressions =          exporter.expressions.selected
        self.bodyShapes =           False # exporter.bodyShapes.selected
        self.useCustomTargets =     exporter.useCustomTargets.selected

        if exporter.rigAdvanced.selected:
            self.rigOptions = ArmatureOptions()
            self.rigOptions.loadPreset("advanced", None, folder="plugins/9_export_mhx")
        elif exporter.rigRigify.selected:
            self.rigOptions = RigifyOptions(self)
        else:
            self.rigOptions = exporter.getRigOptions()
            if not self.rigOptions:
                self.rigOptions = ArmatureOptions()

        if not exporter.rigRigify.selected:
            self.rigOptions.setExportOptions(
                useCustomShapes = True,
                useConstraints = True,
                useBoneGroups = True,
                useCorrectives = self.bodyShapes,
                useExpressions = self.expressions,
                feetOnGround = self.feetOnGround,
                useMasks = self.useMasks,
                useTPose = self.useTPose,
                useLeftRight = False,
            )


class ExporterMHX(Exporter):
    def __init__(self):
        Exporter.__init__(self)
        self.name = "Blender exchange (mhx)"
        self.filter = "Blender Exchange (*.mhx)"
        self.fileExtension = "mhx"

    def build(self, options, taskview):
        self.taskview       = taskview
        self.useTexFolder   = options.addWidget(gui.CheckBox("Separate texture folder", True))
        self.feetOnGround   = options.addWidget(gui.CheckBox("Feet on ground", True))
        self.expressions    = options.addWidget(gui.CheckBox("Expressions", False))
        # self.facepanel      = options.addWidget(gui.CheckBox("Face rig", False))
        # self.bodyShapes     = options.addWidget(gui.CheckBox("Body shapes", False))
        self.useCustomTargets = options.addWidget(gui.CheckBox("Custom targets", False))
        #self.masks          = options.addWidget(gui.CheckBox("Clothes masks", False))
        #self.clothesRig     = options.addWidget(gui.CheckBox("Clothes rig", False))
        #self.cage           = options.addWidget(gui.CheckBox("Cage", False))
        #self.advancedSpine  = options.addWidget(gui.CheckBox("Advanced spine", False))
        #self.maleRig        = options.addWidget(gui.CheckBox("Male rig", False))

        rigs = []
        self.rigAdvanced     = options.addWidget(gui.RadioButton(rigs, "Advanced rig", True))
        self.rigRigify       = options.addWidget(gui.RadioButton(rigs, "Rigify rig", False))
        self.rigFromLibrary  = options.addWidget(gui.RadioButton(rigs, "Use rig from library", False))


    def export(self, human, filename):
        from . import mhx_main
        #from mhx import mhx_main
        self.taskview.exitPoseMode()
        mhx_main.exportMhx(human, filename("mhx"), MhxConfig(self))
        self.taskview.enterPoseMode()


def load(app):
    app.addExporter(ExporterMHX())

def unload(app):
    pass
