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

import gui
from export import Exporter
from exportutils.config import Config


class FbxConfig(Config):

    def __init__(self, exporter):
        from armature.options import ArmatureOptions

        Config.__init__(self)
        self.selectedOptions(exporter)

        self.useRelPaths     = False
        self.feetOnGround = False
        self.expressions = exporter.expressions.selected
        self.useCustomTargets = exporter.useCustomTargets.selected
        self.useMaterials    = True # for debugging

        self.rigOptions = exporter.getRigOptions()
        if not self.rigOptions:
            self.rigOptions = ArmatureOptions()
        self.rigOptions.setExportOptions(
            useExpressions = self.expressions,
            feetOnGround = self.feetOnGround,
            useTPose = self.useTPose,
            useLeftRight = False,
        )



    def __repr__(self):
        return("<FbxConfig %s s %s e %s h %s>" % (
            self.rigOptions.rigtype, self.useTexFolder, self.expressions, self.helpers))


class ExporterFBX(Exporter):
    def __init__(self):
        Exporter.__init__(self)
        self.name = "Filmbox (fbx)"
        self.filter = "Filmbox (*.fbx)"

    def build(self, options, taskview):
        Exporter.build(self, options, taskview)
        self.expressions     = options.addWidget(gui.CheckBox("Expressions", False))
        self.useCustomTargets = options.addWidget(gui.CheckBox("Custom targets", False))

    def export(self, human, filename):
        from . import mh2fbx
        self.taskview.exitPoseMode()
        mh2fbx.exportFbx(human, filename("fbx"), FbxConfig(self))
        self.taskview.enterPoseMode()


def load(app):
    app.addExporter(ExporterFBX())

def unload(app):
    pass
