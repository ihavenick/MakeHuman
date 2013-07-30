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

Armature options

"""

import os
import gui
import io_json
import mh

class ArmatureOptions:
    def __init__(self):

        self.rigtype = "Default"
        self.description = ""
        self.locale = None
        self.scale = 1.0
        self.boneMap = None

        self.useMasterBone = False
        self.useHeadControl = False
        self.useReverseHip = False
        self.useMuscles = False
        self.useRotationLimits = False
        self.addConnectingBones = False

        self.mergeSpine = False
        self.mergeShoulders = False
        self.mergeFingers = False
        self.mergePalms = False
        self.mergeHead = False
        self.merge = None

        self.useSplitBones = False
        self.useSplitNames = False
        self.useDeformBones = False
        self.useDeformNames = False
        self.useIkArms = False
        self.useIkLegs = False
        self.useFingers = False

        # Options set by exporters
        self.useCustomShapes = False
        self.useConstraints = False
        self.useBoneGroups = False
        self.useCorrectives = False
        self.useExpressions = False
        self.feetOnGround = False
        self.useMasks = False
        self.useTPose = False
        self.useLeftRight = False

        # Obsolete options once used by mhx
        self.facepanel = False
        self.advancedSpine = False
        self.clothesRig = False


    def setExportOptions(self,
            useCustomShapes = False,
            useConstraints = False,
            useBoneGroups = False,
            useCorrectives = False,
            useExpressions = False,
            feetOnGround = False,
            useMasks = False,
            useTPose = False,
            useLeftRight = False,
            ):
        self.useCustomShapes = useCustomShapes
        self.useConstraints = useConstraints
        self.useBoneGroups = useBoneGroups
        self.useCorrectives = useCorrectives
        self.useExpressions = useExpressions
        self.feetOnGround = feetOnGround
        self.useMasks = useMasks
        self.useTPose = useTPose
        self.useLeftRight = useLeftRight


    def __repr__(self):
        return (
            "<ArmatureOptions\n" +
            "   rigtype : %s\n" % self.rigtype +
            "   description : %s\n" % self.description +
            "   scale : %s\n" % self.scale +
            "   boneMap : %s\n" % self.boneMap +
            "   useMuscles : %s\n" % self.useMuscles +
            "   addConnectingBones : %s\n" % self.addConnectingBones +
            "   mergeSpine : %s\n" % self.mergeSpine +
            "   mergeShoulders : %s\n" % self.mergeShoulders +
            "   mergeFingers : %s\n" % self.mergeFingers +
            "   mergePalms : %s\n" % self.mergePalms +
            "   mergeHead : %s\n" % self.mergeHead +
            "   useSplitBones : %s\n" % self.useSplitBones +
            "   useSplitNames : %s\n" % self.useSplitNames +
            "   useDeformBones : %s\n" % self.useDeformBones +
            "   useDeformNames : %s\n" % self.useDeformNames +
            "   useIkArms : %s\n" % self.useIkArms +
            "   useIkLegs : %s\n" % self.useIkLegs +
            "   useFingers : %s\n" % self.useFingers +
            "   useMasterBone : %s\n" % self.useMasterBone +
            "   useCorrectives : %s\n" % self.useCorrectives +
            "   feetOnGround : %s\n" % self.feetOnGround +
            "   useMasks : %s\n" % self.useMasks +
            "   merge : %s\n" % self.merge +
            "   locale : %s\n" % self.locale +
            ">")


    def fromSelector(self, selector):
        self.useMuscles = selector.useMuscles.selected
        self.useReverseHip = selector.useReverseHip.selected
        #self.useCorrectives = selector.useCorrectives.selected
        self.useRotationLimits = selector.useRotationLimits.selected
        self.addConnectingBones = selector.addConnectingBones.selected

        self.mergeSpine = selector.mergeSpine.selected
        self.mergeShoulders = selector.mergeShoulders.selected
        self.mergeFingers = selector.mergeFingers.selected
        self.mergePalms = selector.mergePalms.selected
        self.mergeHead = selector.mergeHead.selected

        self.useSplitBones = selector.useSplitBones.selected
        self.useSplitNames = selector.useSplitBones.selected
        self.useIkArms = selector.useIkArms.selected
        self.useIkLegs = selector.useIkLegs.selected
        self.useDeformBones = selector.useDeformBones.selected
        self.useDeformNames = selector.useDeformBones.selected

        self.useMasterBone = selector.useMasterBone.selected


    def reset(self, selector):
        self.__init__()
        selector.fromOptions(self)


    def loadPreset(self, filename, selector, folder=mh.getSysDataPath("rigs/")):
        filepath = os.path.join(folder, filename + ".json")
        struct = io_json.loadJson(filepath)
        self.__init__()
        try:
            self.rigtype = struct["name"]
        except KeyError:
            pass
        try:
            self.description = struct["description"]
        except KeyError:
            pass
        try:
            self.merge = struct["merge"]
        except KeyError:
            pass
        try:
            settings = struct["settings"]
        except KeyError:
            settings = {}
        for key,value in list(settings.items()):
            expr = ("self.%s = %s" % (key, value))
            exec(expr)

        if selector is not None:
            selector.fromOptions(self)
        try:
            bones = struct["bones"]
        except KeyError:
            bones = None
        if bones:
            self.locale = Locale(bones=bones)
        return self.description


class ArmatureSelector:

    def __init__(self, box):
        self.box = box

        self.useMuscles = box.addWidget(gui.ToggleButton("Muscle bones (MHX only)"))
        self.useReverseHip = box.addWidget(gui.ToggleButton("Reverse hips"))
        self.addConnectingBones = box.addWidget(gui.ToggleButton("Connecting bones"))
        self.useRotationLimits = box.addWidget(gui.ToggleButton("Use rotation limits (MHX only)"))

        self.mergeSpine = box.addWidget(gui.ToggleButton("Merge spine"))
        self.mergeShoulders = box.addWidget(gui.ToggleButton("Merge shoulders"))
        self.mergeFingers = box.addWidget(gui.ToggleButton("Merge fingers"))
        self.mergePalms = box.addWidget(gui.ToggleButton("Merge palms"))
        self.mergeHead = box.addWidget(gui.ToggleButton("Merge head"))

        self.useSplitBones = box.addWidget(gui.ToggleButton("Split forearm (MHX only)"))
        self.useDeformBones = box.addWidget(gui.ToggleButton("Deform bones (MHX only)"))
        self.useIkArms = box.addWidget(gui.ToggleButton("Arm IK (MHX only)"))
        self.useIkLegs = box.addWidget(gui.ToggleButton("Leg IK (MHX only)"))
        self.useFingers = box.addWidget(gui.ToggleButton("Finger controls (MHX only)"))

        self.useMasterBone = box.addWidget(gui.ToggleButton("Master bone"))


    def fromOptions(self, options):
        self.useMuscles.setSelected(options.useMuscles)
        self.useReverseHip.setSelected(options.useReverseHip)
        self.addConnectingBones.setSelected(options.addConnectingBones)
        self.useRotationLimits.setSelected(options.useRotationLimits)

        self.mergeSpine.setSelected(options.mergeSpine)
        self.mergeShoulders.setSelected(options.mergeShoulders)
        self.mergeFingers.setSelected(options.mergeFingers)
        self.mergePalms.setSelected(options.mergePalms)
        self.mergeHead.setSelected(options.mergeHead)

        self.useSplitBones.setSelected(options.useSplitBones)
        self.useDeformBones.setSelected(options.useDeformBones)
        self.useIkArms.setSelected(options.useIkArms)
        self.useIkLegs.setSelected(options.useIkLegs)
        self.useFingers.setSelected(options.useFingers)

        self.useMasterBone.setSelected(options.useMasterBone)

        for child in self.box.children:
            child.update()


class Locale:
    def __init__(self, filepath=None, bones=[]):
        self.filepath = filepath
        self.bones = bones


    def __repr__(self):
        string = "<Locale %s:" % (self.filepath)
        #for key,bone in self.bones.items():
        #    string += "\n    %s %s" % (key,bone)
        return string + ">"


    def load(self, filepath=None):
        if self.bones:
            return
        if filepath:
            self.filepath = filepath
        struct = io_json.loadJson(self.filepath)
        #self.language = struct["language"]
        self.bones = struct["bones"]


    def rename(self, bname):
        if bname[0:4] == "DEF-":
            return "DEF-" + self.rename(bname[4:])

        try:
            return self.bones[bname]
        except KeyError:
            pass

        words = bname.split(".", 1)
        try:
            return self.bones[words[0]] + "." + words[1]
        except KeyError:
            return bname

