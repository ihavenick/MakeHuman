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

Base armature
"""

import math
import log
from collections import OrderedDict

import numpy as np
import numpy.linalg as la
import transformations as tm

from .flags import *
from .utils import *

#-------------------------------------------------------------------------------
#   Setup Armature
#-------------------------------------------------------------------------------

def setupArmature(name, human, options):
    from .parser import Parser
    if options is None:
        return None
    else:
        log.message("Setup rig %s" % name)
        amt = Armature(name, options)
        amt.parser = Parser(amt, human)
        amt.setup()
        log.message("Using rig with options %s" % options)
        return amt

#-------------------------------------------------------------------------------
#   Armature base class.
#-------------------------------------------------------------------------------

class Armature:

    def __init__(self, name, options):
        self.name = name
        self.options = options
        self.parser = None
        self.origin = None
        self.roots = []
        self.bones = OrderedDict()
        self.hierarchy = []
        self.locale = None

        self.done = False

        self.vertexWeights = OrderedDict([])
        self.isNormalized = False


    def __repr__(self):
        return ("  <BaseArmature %s %s>" % (self.name, self.options.rigtype))


    def setup(self):
        self.parser.setup()
        self.origin = self.parser.origin
        self.rename(self.options.locale)


    def rescale(self, scale):
        # OK to overwrite bones, because they are not used elsewhere
        for bone in list(self.bones.values()):
            bone.rescale(scale)


    def rename(self, locale):
        if self.locale == locale:
            return
        self.locale = locale
        if locale:
            locale.load()

        newbones = OrderedDict()
        for bone in list(self.bones.values()):
            bone.rename(locale, newbones)
        self.bones = newbones

        for bname,vgroup in list(self.vertexWeights.items()):
            newname = locale.rename(bname)
            if newname != bname:
                self.vertexWeights[newname] = vgroup
                del self.vertexWeights[bname]


    def normalizeVertexWeights(self, human):
        if self.isNormalized:
            return

        nVerts = len(human.meshData.coord)
        wtot = np.zeros(nVerts, float)
        for vgroup in list(self.vertexWeights.values()):
            for vn,w in vgroup:
                wtot[vn] += w

        for bname in list(self.vertexWeights.keys()):
            vgroup = self.vertexWeights[bname]
            weights = np.zeros(len(vgroup), float)
            verts = []
            n = 0
            for vn,w in vgroup:
                verts.append(vn)
                weights[n] = w/wtot[vn]
                n += 1
            self.vertexWeights[bname] = (verts, weights)

        self.isNormalized = True


    def calcBindMatrices(self):
        import io_json
        self.bindMatrix = tm.rotation_matrix(math.pi/2, XUnit)
        self.bindInverse = la.inv(self.bindMatrix)

        if self.options.useTPose:
            filepath = "tools/blender26x/mh_mocap_tool/t_pose.json"
            blist = io_json.loadJson(filepath)
            for bname,quat in blist:
                pmat = tm.quaternion_matrix(quat)
                log.debug("TPose %s %s" % ( bname, pmat))
                self.bones[bname].matrixTPose = pmat
        else:
            for bone in list(self.bones.values()):
                bone.matrixTPose = None

        for bone in list(self.bones.values()):
            bone.calcBindMatrix()


class Bone:
    def __init__(self, amt, name):
        self.name = name
        self.origName = name
        self.type = "LimbNode"
        self.armature = amt
        self.head = None
        self.tail = None
        self.roll = 0
        self.parent = None
        self.setFlags(0)
        self.layers = L_MAIN
        self.length = 0
        self.customShape = None
        self.children = []

        self.location = (0,0,0)
        self.lockLocation = (0,0,0)
        self.lockRotation = (0,0,0)
        self.lockScale = (1,1,1)
        self.ikDof = (1,1,1)
        #self.lock_rotation_w = False
        #self.lock_rotations_4d = False

        self.constraints = []
        self.drivers = []

        # Matrices:
        # matrixRest:       4x4 rest matrix, relative world
        # matrixRelative:   4x4 rest matrix, relative parent
        # matrixPose:       4x4 pose matrix, relative parent and own rest pose
        # matrixGlobal:     4x4 matrix, relative world
        # matrixVerts:      4x4 matrix, relative world and own rest pose

        self.matrixRest = None
        self.matrixRelative = None
        self.bindMatrix = None
        self.bindInverse = None
        self.matrixTPose = None
        self.matrixPosedRest = None


    def __repr__(self):
        return "<Bone %s %s %s>" % (self.name, self.parent, self.children)


    def fromInfo(self, info):
        self.roll, self.parent, flags, self.layers = info
        if self.parent and not flags & F_NOLOCK:
            self.lockLocation = (1,1,1)
        self.setFlags(flags)
        if self.roll == None:
            halt


    def setFlags(self, flags):
        self.flags = flags
        self.conn = (flags & F_CON != 0)
        self.deform = (flags & F_DEF != 0)
        self.restr = (flags & F_RES != 0)
        self.wire = (flags & F_WIR != 0)
        self.lloc = (flags & F_NOLOC == 0)
        self.lock = (flags & F_LOCK != 0)
        self.cyc = (flags & F_NOCYC == 0)
        self.hide = (flags & F_HID)
        self.norot = (flags & F_NOROT)
        self.scale = (flags & F_SCALE)


    def setBone(self, head, tail):
        self.head = head
        self.tail = tail
        vec = tail - head
        self.length = math.sqrt(np.dot(vec,vec))

        if isinstance(self.roll, str):
            if self.roll[0:5] == "Plane":
                normal = m2b(self.armature.parser.normals[self.roll])
                self.roll = computeRoll(self.head, self.tail, normal, bone=self)


    def rescale(self, scale):
        self.head = scale*self.head
        self.tail = scale*self.tail
        self.length = scale*self.length

        self.matrixRest = None
        self.matrixRelative = None
        self.bindMatrix = None
        self.bindInverse = None


    def rename(self, locale, newbones):
        amt = self.armature
        self.name = renameBone(self, locale)
        if self.parent:
            self.parent = renameBone(amt.bones[self.parent], locale)
        for cns in self.constraints:
            if cns.type in ["Transform", "StretchTo", "TrackTo", "IK"]:
                cns.subtar = renameBone(amt.bones[cns.subtar], locale)
        newbones[self.name] = self


    def calcRestMatrix(self):
        if self.matrixRest is not None:
            return

        _,self.matrixRest = getMatrix(self.head, self.tail, self.roll)

        if self.parent:
            parbone = self.armature.bones[self.parent]
            self.matrixRelative = np.dot(la.inv(parbone.matrixRest), self.matrixRest)
        else:
            self.matrixRelative = self.matrixRest


    def getBindMatrixCollada(self):
        self.calcRestMatrix()
        rotX = tm.rotation_matrix(math.pi/2, XUnit)
        mat4 = np.dot(rotX, self.matrixRest)
        return la.inv(mat4)


    def calcBindMatrix(self):
        if self.bindMatrix is not None:
            return

        self.calcRestMatrix()

        if self.matrixTPose is None:
            self.matrixPosedRest = self.matrixRest
        else:
            self.matrixPosedRest = np.dot(self.matrixRest, self.matrixTPose)
            if self.parent:
                parbone = self.armature.bones[self.parent]
                self.matrixRelative = np.dot(la.inv(parbone.matrixPosedRest), self.matrixPosedRest)
            else:
                self.matrixRelative = self.matrixRest
            log.debug("TM %s" % self.name)

        self.bindInverse = np.transpose(self.matrixRest)
        self.bindMatrix = la.inv(self.bindInverse)


def renameBone(bone, locale):
    if locale:
        return locale.rename(bone.name)
    else:
        return bone.origName





