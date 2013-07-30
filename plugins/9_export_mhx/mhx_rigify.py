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

Definitions for the Rigify rig, which is intended for use with Blender's Rigify plugin.
Only works with MHX export.

"""

from armature.parser import Parser
from armature.options import ArmatureOptions, Locale
from .mhx_armature import ExportArmature
from armature import rig_bones


class RigifyArmature(ExportArmature):

    def __init__(self, name, options):
        ExportArmature.__init__(self, name, options)
        self.visibleLayers = "08a80caa"
        self.recalcRoll = []
        self.objectProps = [("MhxRig", '"Rigify"')]


    def writeFinal(self, fp):
        fp.write('Rigify %s ;\n' % self.name)


class RigifyOptions(ArmatureOptions):
    def __init__(self, config):
        ArmatureOptions.__init__(self)

        self.description = (
"""
A rig intended for use with Blender's Rigify plugin.
Only works with MHX export.
""")

        self.useMuscles = True
        self.useSplitNames = True
        self.useDeformNames = True
        self.mergeShoulders = False

        # Options set by MHX exporter
        self.useCustomShapes = False
        self.useConstraints = True
        self.useRotationLimits = False
        self.useBoneGroups = False
        self.useCorrectives = config.bodyShapes
        self.useExpressions = config.expressions
        self.feetOnGround = config.feetOnGround
        self.useMasks = config.useMasks

        renameBones = {
            "palm_index.L" : "palm.01.L",
            "palm_middle.L" : "palm.02.L",
            "palm_ring.L" : "palm.03.L",
            "palm_pinky.L" : "palm.04.L",

            "palm_index.R" : "palm.01.R",
            "palm_middle.R" : "palm.02.R",
            "palm_ring.R" : "palm.03.R",
            "palm_pinky.R" : "palm.04.R",
        }
        self.locale = Locale(bones=renameBones)



class RigifyParser(Parser):

    def __init__(self, amt, human):
        Parser.__init__(self, amt, human)

        self.splitBones = {
            "upper_arm" :   (2, "forearm", False),
            "forearm" :     (2, "hand", False),
            "thigh" :       (2, "shin", False),
            "shin" :        (2, "foot", False),

            "thumb.01" :    (2, "thumb.02", True),
            "f_index.01" :  (2, "f_index.02", True),
            "f_middle.01" : (2, "f_middle.02", True),
            "f_ring.01" :   (2, "f_ring.02", True),
            "f_pinky.01" :  (2, "f_pinky.02", True),
        }

        self.objectProps = (
            rig_bones.ObjectProps +
            [("MhxRig", '"Rigify"'),
             ("MhxRigify", True)]
        )

