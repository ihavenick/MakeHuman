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

__docformat__ = 'restructuredtext'

import math
import numpy as np
from operator import mul
import mh
import os

import algos3d
import meshstat
import warp
import humanmodifier
import log
from core import G

#----------------------------------------------------------
#   class WarpTarget
#----------------------------------------------------------

class WarpTarget(algos3d.Target):

    def __init__(self, modifier, human):

        algos3d.Target.__init__(self, human.meshData, modifier.warppath)

        self.human = human
        self.modifier = modifier
        self.isDirty = True
        self.isObsolete = False


    def __repr__(self):
        return ( "<WarpTarget %s dirty:%s>" % (os.path.basename(self.modifier.warppath), self.isDirty) )


    def reinit(self):

        if self.isDirty:
            shape = self.modifier.compileWarpTarget(self.human)
            saveWarpedTarget(shape, self.modifier.warppath)
            self.__init__(self.modifier, self.human)
            self.isDirty = False


    def apply(self, obj, morphFactor, update=True, calcNormals=True, faceGroupToUpdateName=None, scale=(1.0,1.0,1.0)):

        self.reinit()
        algos3d.Target.apply(self, obj, morphFactor, update, calcNormals, faceGroupToUpdateName, scale)


def saveWarpedTarget(shape, path):
    slist = list(shape.items())
    slist.sort()
    fp = open(path, "w")
    for (n, dr) in slist:
        fp.write("%d %.4f %.4f %.4f\n" % (n, dr[0], dr[1], dr[2]))
    fp.close()

#----------------------------------------------------------
#   class WarpModifier
#----------------------------------------------------------

class BaseSpec:
    def __init__(self, path, factors):
        self.path = path
        self.factors = factors
        self.value = -1

    def __repr__(self):
        return ("<BaseSpec %s %.4f %s>" % (self.path, self.value, self.factors))


class TargetSpec:
    def __init__(self, path, factors):
        self.path = path.replace("-${tone}","").replace("-${weight}","")
        self.factors = factors
        if "$" in self.path:
            log.debug("TS %s %s" % (self.path, path))
            halt

    def __repr__(self):
        return ("<TargetSpec %s %s>" % (self.path, self.factors))


class WarpModifier (humanmodifier.SimpleModifier):

    def __init__(self, template, bodypart, modtype):
        global _warpGlobals

        string = template.replace('$','').replace('{','').replace('}','')
        warppath = os.path.join(mh.getPath(""), "warp", string)
        if not os.path.exists(os.path.dirname(warppath)):
            os.makedirs(os.path.dirname(warppath))
        if not os.path.exists(warppath):
            fp = open(warppath, "w")
            fp.close()

        humanmodifier.SimpleModifier.__init__(self, warppath)
        self.eventType = 'warp'
        self.warppath = warppath
        self.template = template
        self.bodypart = bodypart
        self.slider = None
        self.refTargets = {}
        self.refTargetVerts = {}
        self.modtype = modtype

        self.fallback = None
        for (tlabel, tname, tvar) in _warpGlobals.modifierTypes[modtype]:
            self.fallback = humanmodifier.MacroModifier(tlabel, tname, tvar)
            break

        self.remaps = {}
        for ethnic in _warpGlobals.ethnics:
            self.remaps[ethnic] = ethnic
        for age in _warpGlobals.ages:
            self.remaps[age] = age
        for gender in _warpGlobals.genders:
            self.remaps[gender] = gender

        self.bases = {}
        self.targetSpecs = {}
        if modtype == "GenderAge":
            self.setupBaseCharacters("Gender", "Age", "NoEthnic", "NoUniv", "NoUniv")
        elif modtype == "Ethnic":
            self.setupBaseCharacters("NoGender", "NoAge", "Ethnic", "NoUniv", "NoUniv")
        elif modtype == "GenderAgeEthnic":
            self.setupBaseCharacters("Gender", "Age", "Ethnic", "NoUniv", "NoUniv")
        elif modtype == "GenderAgeToneWeight":
            self.setupBaseCharacters("Gender", "Age", "NoEthnic", "Tone", "Weight")


    def setupBaseCharacters(self, genders, ages, ethnics, tones, weights):
        global _warpGlobals

        for gender in _warpGlobals.baseCharacterParts[genders]:
            for age in _warpGlobals.baseCharacterParts[ages]:
                for ethnic in _warpGlobals.baseCharacterParts[ethnics]:
                    path1 = str(self.template)
                    key1 = ""
                    factors1 = []
                    base1 = mh.getSysDataPath("targets/macrodetails/")

                    if ethnic is None:
                        base1 += "caucasian-"
                        for e in _warpGlobals.ethnics:
                            self.remaps[e] = "caucasian"
                    else:
                        base1 += ethnic + "-"
                        key1 += ethnic + "-"
                        factors1.append(ethnic)
                        path1 = path1.replace("${ethnic}", ethnic)

                    if True:    # Hack for expressions
                        for e in _warpGlobals.ethnics:
                            self.remaps[e] = "caucasian"

                    if gender is None:
                        base1 += "female-"
                        for g in _warpGlobals.genders:
                            self.remaps[g] = "female"
                    else:
                        base1 += gender + "-"
                        key1 += gender + "-"
                        factors1.append(gender)
                        path1 = path1.replace("${gender}", gender)

                    if age is None:
                        base1 += "young.target"
                        for a in _warpGlobals.ages:
                            self.remaps[a] = "young"
                    else:
                        base1 += age + ".target"
                        key1 += age
                        factors1.append(age)
                        path1 = path1.replace("${age}", age)

                    if key1[-1] == "-":
                        key1 = key1[:-1]
                    self.bases[key1] = BaseSpec(base1, factors1)
                    self.targetSpecs[key1] = TargetSpec(path1, factors1)
                    if gender is None or age is None:
                        #log.debug("Bases %s" % self.bases.items())
                        return

                    for tone in _warpGlobals.baseCharacterParts[tones]:
                        for weight in _warpGlobals.baseCharacterParts[weights]:
                            if tone and weight:
                                tone2 = tone
                                weight2 = weight
                            '''
                            elif tone:
                                tone2 = tone
                                weight2 = "averageweight"
                            elif tone:
                                tone2 = "averagemuscle"
                                weight2 = weight
                            else:
                                tone2 = "averagemuscle"
                                weight2 = "averageweight"
                            '''
                            base2 = mh.getSysDataPath("targets/macrodetails/universal-%s-%s-%s-%s.target") % (gender, age, tone, weight)
                            key2 = "universal-%s-%s-%s-%s" % (gender, age, tone2, weight2)
                            factors2 = factors1 + [tone2, weight2]
                            self.bases[key2] = BaseSpec(base2, factors2)
                            path2 = path1.replace("${tone}", tone2).replace("${weight}", weight2)
                            self.targetSpecs[key2] = TargetSpec(path2, factors2)

                            '''
                            elif tone:
                                base2 = mh.getSysDataPath("targets/macrodetails/universal-%s-%s-%s-averageweight.target") % (gender, age, tone)
                                key2 = "universal-%s-%s-%s" % (gender, age, tone)
                                factors2 = factors1 + [tone, 'averageweight']
                                self.bases[key2] = BaseSpec(base2, factors2)
                                path2 = path1.replace("${tone}", tone).replace("-${weight}", "")
                                self.targetSpecs[key2] = TargetSpec(path2, factors2)

                            elif weight:
                                base2 = mh.getSysDataPath("targets/macrodetails/universal-%s-%s-averagemuscle-%s.target") % (gender, age, weight)
                                key2 = "universal-%s-%s-%s" % (gender, age, weight)
                                factors2 = factors1 + ['averagemuscle', weight]
                                self.bases[key2] = BaseSpec(base2, factors2)
                                path2 = path1.replace("-${tone}", "").replace("${weight}", weight)
                                self.targetSpecs[key2] = TargetSpec(path2, factors2)

                            else:
                                base2 = mh.getSysDataPath("targets/macrodetails/universal-%s-%s-averagemuscle-averageweight.target") % (gender, age)
                                key2 = "universal-%s" % (gender)
                                factors2 = factors1 + ['averagemuscle', 'averageweight']
                                path2 = path1.replace("-${tone}", "").replace("-${weight}", "")
                                self.targetSpecs[key1] = TargetSpec(path2, factors2)
                            '''



    def __repr__(self):
        return ("<WarpModifier %s>" % (os.path.basename(self.template)))


    def setValue(self, human, value):
        self.compileTargetIfNecessary(human)
        humanmodifier.SimpleModifier.setValue(self, human, value)


    def updateValue(self, human, value, updateNormals=1):
        self.compileTargetIfNecessary(human)
        humanmodifier.SimpleModifier.updateValue(self, human, value, updateNormals)
        human.warpNeedReset = False


    def clampValue(self, value):
        return max(0.0, min(1.0, value))


    def compileTargetIfNecessary(self, human):
        try:
            target = algos3d.warpTargetBuffer[self.warppath]
        except KeyError:
            target = None
        if target:
            if not isinstance(target, WarpTarget):
                raise NameError("%s is not a warp target" % target)
        else:
            target = WarpTarget(self, human)
            algos3d.warpTargetBuffer[self.warppath] = target

        target.reinit()


    def compileWarpTarget(self, human):
        global _warpGlobals
        log.message("COMPWARP %s", self)
        landmarks = _warpGlobals.getLandMarks(self.bodypart)

        obj = human.meshData
        srcCharCoord = obj.orig_coord.copy()
        trgCharCoord = obj.orig_coord.copy()

        for trgpath,value in human.targetsDetailStack.items():
            try:
                target = algos3d.targetBuffer[trgpath]
            except KeyError:
                continue
            srcVerts = np.s_[...]
            dstVerts = target.verts[srcVerts]
            data = value * target.data[srcVerts]
            data.resize((meshstat.numberOfVertices,3))
            trgCharCoord += data
            if trgpath in self.bases.keys():
                srcCharCoord[dstVerts] += data

        self.updateRefTarget(human)

        if self.refTargetVerts:
            shape = warp.warp_target(self.refTargetVerts, srcCharCoord, trgCharCoord, landmarks)
        else:
            shape = {}
        log.message("...done")
        return shape


    def updateRefTarget(self, human):
        if not self.makeRefTarget(human):
            log.message("Updating character")
            #human.applyAllTargets()
            self.getBases(human)
            if not self.makeRefTarget(human):
                raise NameError("Character is empty")


    def getBases(self, human):
        targetChanged = False
        for key,base in self.bases.items():
            verts = self.getRefObjectVerts(base.path)
            if verts is None:
                base.value = 0
                continue

            cval1 = human.getDetail(base.path)
            if base.value != cval1:
                base.value = cval1
                targetChanged = True
        return targetChanged


    def makeRefTarget(self, human):
        self.refTargetVerts = {}
        madeRefTarget = False

        factors = {}
        for key,value in self.fallback.getFactors(human, 1.0).items():
            try:
                key1 = self.remaps[key]
            except KeyError:
                key1 = key
            try:
                factors[key1] += value
            except KeyError:
                factors[key1] = value

        for target in self.targetSpecs.values():
            cval = 1.0
            for factor in target.factors:
                cval *= factors[factor]
            if cval > 1e-6:
                madeRefTarget = True
                verts = self.getRefTargetVertsInsist(target.path)
                if verts is not None:
                    addVerts(self.refTargetVerts, cval, verts)
        return madeRefTarget


    def getRefTargetVertsInsist(self, path):
        verts = self.getTarget(path)
        if verts is not None:
            self.refTargets[path] = verts
            return verts

        for string in ["minmuscle", "maxmuscle", "minweight", "maxweight"]:
            if string in path:
                log.message("  Did not find %s", path)
                return None

        path1 = path.replace("/asian", "/caucasian").replace("/african", "/caucasian")
        verts = self.getTarget(path1)
        if verts is not None:
            self.refTargets[path] = verts
            log.message("   Replaced %s\n  -> %s", path, path1)
            return verts

        path2 = path1.replace("/baby", "/young").replace("/child", "/young").replace("/old", "/young")
        verts = self.getTarget(path2)
        if verts is not None:
            self.refTargets[path] = verts
            log.message("   Replaced %s\n  -> %s", path, path2)
            return verts

        path3 = path2.replace("/male", "/female")
        if verts is not None:
            self.refTargets[path] = verts
            log.message("   Replaced %s\n  -> %s", path, path2)
            return verts

        path4 = path3.replace("/female_young", "")
        verts = self.getTarget(path4)
        self.refTargets[path] = verts

        if verts is None:
            log.message("Warning: Found none of:\n    %s\n    %s\n    %s\n    %s\n    %s" %
                (path, path1, path2, path3, path4))
        else:
            log.message("   Replaced %s\n  -> %s" % (path, path4))
        return verts


    def getTarget(self, path):
        try:
            verts = self.refTargets[path]
        except KeyError:
            verts = None
        if verts is None:
            verts = readTarget(path)
        return verts

#----------------------------------------------------------
#   Call from exporter
#----------------------------------------------------------

def compileWarpTarget(template, fallback, human, bodypart):
    mod = WarpModifier(template, bodypart, fallback)
    return mod.compileWarpTarget(human)

#----------------------------------------------------------
#   Read target
#----------------------------------------------------------

def readTarget(filepath):

    words = filepath.split("-")
    if (words[0] == mh.getSysDataPath("targets/macrodetails/universal") and
        words[-2] == "averagemuscle" and
        words[-1] == "averageweight.target"):
        return {}

    try:
        fp = open(filepath, "r")
    except:
        fp = None

    if fp is None:
        filepath1 = filepath.replace("-averagemuscle", "").replace("-averageweight", "")
        try:
            fp = open(filepath1, "r")
        except:
            fp = None

    if fp:
        target = {}
        for line in fp:
            words = line.split()
            if len(words) >= 4 and words[0][0] != '#':
                n = int(words[0])
                if n < meshstat.numberOfVertices:
                    target[n] = np.array([float(words[1]), float(words[2]), float(words[3])])
        fp.close()
        return target
    else:
        log.message("Found neither %s nor %s" % (filepath, filepath1))
        halt
        return None

#----------------------------------------------------------
#   For testing np
#----------------------------------------------------------

def addVerts(targetVerts, cval, verts):
    for n,v in verts.items():
        dr = cval*v
        try:
            targetVerts[n] += dr
        except KeyError:
            targetVerts[n] = dr

#----------------------------------------------------------
#   Global warp data
#----------------------------------------------------------

class GlobalWarpData:
    def __init__(self):
        self._refObjectVerts = None
        self._landMarks = None
        self._refObjects = None
        self._unwarpedCoords = None
        self._warpedCoords = None
        self.dirty = False

        self.ethnics = ["african", "asian", "caucasian"]
        self.genders = ["female", "male"]
        self.ages = ["baby", "child", "young", "old"]

        self.modifierTypes = {
            "GenderAge" : [
                ("macrodetails", None, "Gender"),
                ("macrodetails", None, "Age"),
            ],
            "Ethnic" : [
                ("macrodetails", None, "African"),
                ("macrodetails", None, "Asian"),
            ],
            "GenderAgeEthnic" : [
                ("macrodetails", None, "Gender"),
                ("macrodetails", None, "Age"),
                ("macrodetails", None, "African"),
                ("macrodetails", None, "Asian"),
            ],
            "GenderAgeToneWeight" : [
                ("macrodetails", None, "Gender"),
                ("macrodetails", None, "Age"),
                ("macrodetails", "universal", "Muscle"),
                ("macrodetails", "universal", "Weight"),
                #("macrodetails", "universal-stature", "Height"),
            ],
        }

        self.baseCharacterParts = {
            "Gender" : ("male", "female"),
            "NoGender" : [None],
            "Age" : ("child", "young", "old"),
            "NoAge" : [None],
            "Ethnic" : ("caucasian", "african", "asian"),
            "NoEthnic" : [None],
            "Tone" : ("minmuscle", "averagemuscle", "maxmuscle"),
            "Weight" : ("minweight", "averageweight", "maxweight"),
            "NoUniv" : [None]
        }


    def reset(self):
        self._unwarpedCoords = None
        self._warpedCoords = None
        self.dirty = False


    def getLandMarks(self, bodypart):
        if self._landMarks is not None:
            return self._landMarks[bodypart]

        self._landMarks = {}
        folder = mh.getSysDataPath("landmarks")
        for file in os.listdir(folder):
            (name, ext) = os.path.splitext(file)
            if ext != ".lmk":
                continue
            path = os.path.join(folder, file)
            with open(path, "r") as fp:
                landmark = []
                for line in fp:
                    words = line.split()
                    if len(words) > 0:
                        m = int(words[0])
                        landmark.append(m)
            self._landMarks[name] = landmark

        return self._landMarks[bodypart]


def touchWarps():
    global _warpGlobals
    _warpGlobals.dirty = True


_warpGlobals = GlobalWarpData()


