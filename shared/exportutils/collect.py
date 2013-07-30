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
MakeHuman to Collada (MakeHuman eXchange format) exporter. Collada files can be loaded into
Blender by collada_import.py.

TODO
"""

import module3d
import mh
import files3d
import os
import time
import numpy
import shutil

import export
import mh2proxy
import richmesh
import log
import catmull_clark_subdivision as cks
import subtextures

from .config import Config

#
#   readTargets(config):
#

from .shapekeys import readExpressionUnits
from .custom import listCustomFiles, readCustomTarget

def readTargets(human, config):
    targets = []
    if config.expressions:
        shapeList = readExpressionUnits(human, 0, 1)
        targets += shapeList

    if config.useCustomTargets:
        files = listCustomFiles(config)

        log.message("Custom shapes:")
        for path,name in files:
            log.message("    %s", path)
            shape = readCustomTarget(path)
            targets.append((name,shape))

    return targets


#
#   setupObjects
#

def setupObjects(name, human, config=None, rawTargets=[], helpers=False, hidden=False, eyebrows=True, lashes=True, subdivide = False, progressCallback=None):
    global theStuff
    from armature.armature import setupArmature

    def progress(prog):
        if progressCallback == None:
            pass
        else:
            progressCallback (prog)

    if not config:
        config = Config()
        config.setHuman(human)

    stuffs = []
    stuff = richmesh.CStuff(name, None, human)
    amt = setupArmature(name, human, config.rigOptions)
    obj = human.meshData
    richMesh = richmesh.getRichMesh(obj, None, None, rawTargets, amt)
    if amt:
        richMesh.weights = amt.vertexWeights

    theStuff = stuff
    deleteGroups = []
    deleteVerts = None  # Don't load deleteVerts from proxies directly, we use the facemask set in the gui module3d
    _,deleteVerts = setupProxies('Clothes', None, human, stuffs, richMesh, config, deleteGroups, deleteVerts)
    _,deleteVerts = setupProxies('Hair', None, human, stuffs, richMesh, config, deleteGroups, deleteVerts)
    _,deleteVerts = setupProxies('Eyes', None, human, stuffs, richMesh, config, deleteGroups, deleteVerts)
    foundProxy,deleteVerts = setupProxies('Proxy', name, human, stuffs, richMesh, config, deleteGroups, deleteVerts)
    progress(0.06*(3-2*subdivide))
    if not foundProxy:
        if helpers:     # helpers override everything
            stuff.richMesh = richMesh
        else:
            stuff.richMesh = filterMesh(richMesh, deleteGroups, deleteVerts, eyebrows, lashes, not hidden)
        stuffs = [stuff] + stuffs

    if config.scale != 1.0:
        amt.rescale(config.scale)
        for stuff in stuffs:
            stuff.richMesh.rescale(config.scale)

    progbase = 0.12*(3-2*subdivide)
    progress(progbase)

    # Subdivide, if requested.
    stuffnum = float(len(stuffs))
    i = 0.0
    for stuff in stuffs:
        progress(progbase+(i/stuffnum)*(1-progbase))
        if subdivide:
            subMesh = cks.createSubdivisionObject(
                stuff.richMesh.object, lambda p: progress(progbase+((i+p)/stuffnum)*(1-progbase)))
            stuff.richMesh.fromObject(subMesh, stuff.richMesh.weights, rawTargets)
        i += 1.0

    # Apply subtextures. Obsolete with separate eyes
    #mhstx = mh.G.app.getCategory('Textures').getTaskByName('Texture').eyeTexture
    #if mhstx:
    #    stuffs[0].material.diffuseTexture = subtextures.combine(
    #        stuffs[0].material.diffuseTexture, mhstx)

    progress(1)
    return stuffs,amt

#
#    setupProxies(typename, name, human, stuffs, richMesh, config, deleteGroups, deleteVerts):
#

def setupProxies(typename, name, human, stuffs, richMesh, config, deleteGroups, deleteVerts):
    # TODO document that this method does not only return values, it also modifies some of the passed parameters (deleteGroups and stuffs, deleteVerts is modified only if it is not None)
    global theStuff

    foundProxy = False
    for proxy in list(config.getProxies().values()):
        if proxy.type == typename:
            foundProxy = True
            deleteGroups += proxy.deleteGroups
            if deleteVerts != None:
                deleteVerts = deleteVerts | proxy.deleteVerts
            if not name:
                name = proxy.name
            stuff = richmesh.CStuff(name, proxy, human)
            if stuff:
                if proxy.type == 'Proxy':
                     theStuff = stuff
                stuffname = theStuff.name if theStuff else None

                stuff.richMesh = richmesh.getRichMesh(None, proxy, richMesh.weights, richMesh.shapes, richMesh.armature)
                stuffs.append(stuff)
    return foundProxy, deleteVerts

#
#
#

def filterMesh(richMesh, deleteGroups, deleteVerts, eyebrows, lashes, useFaceMask = False):
    """
    Filter out vertices and faces from the mesh that are not desired for exporting.
    """
    # DONE. TODO scaling does not belong in a filter method.
    obj = richMesh.object

    killUvs = numpy.zeros(len(obj.texco), bool)
    killFaces = numpy.zeros(len(obj.fvert), bool)

    if deleteVerts is not None:
        killVerts = deleteVerts
        for fn,fverts in enumerate(obj.fvert):
            for vn in fverts:
                if killVerts[vn]:
                    killFaces[fn] = True
    else:
        killVerts = numpy.zeros(len(obj.coord), bool)

    killGroups = []
    for fg in obj.faceGroups:
        if (("joint" in fg.name) or
           ("helper" in fg.name) or
           ((not eyebrows) and
           (("eyebrown" in fg.name) or ("cornea" in fg.name))) or
           ((not lashes) and
           ("lash" in fg.name)) or
           deleteGroup(fg.name, deleteGroups)):
            killGroups.append(fg.name)

    faceMask = obj.getFaceMaskForGroups(killGroups)
    if useFaceMask:
        # Apply the facemask set on the module3d object (the one used for rendering within MH)
        faceMask = numpy.logical_or(faceMask, numpy.logical_not(obj.getFaceMask()))
    killFaces[faceMask] = True

    #verts = obj.fvert[faceMask]
    verts = obj.fvert[numpy.logical_not(faceMask)]
    vertMask = numpy.ones(len(obj.coord), bool)
    vertMask[verts] = False
    verts = numpy.argwhere(vertMask)
    del vertMask
    killVerts[verts] = True

    #uvs = obj.fuvs[faceMask]
    uvs = obj.fuvs[numpy.logical_not(faceMask)]
    uvMask = numpy.ones(len(obj.texco), bool)
    uvMask[uvs] = False
    uvs = numpy.argwhere(uvMask)
    del uvMask
    killUvs[uvs] = True

    n = 0
    newVerts = {}
    coords = []
    for m,co in enumerate(obj.coord):
        if not killVerts[m]:
            coords.append(co)
            newVerts[m] = n
            n += 1

    n = 0
    texVerts = []
    newUvs = {}
    for m,uv in enumerate(obj.texco):
        if not killUvs[m]:
            texVerts.append(uv)
            newUvs[m] = n
            n += 1

    faceVerts = []
    faceUvs = []
    for fn,fverts in enumerate(obj.fvert):
        if not killFaces[fn]:
            fverts2 = []
            fuvs2 = []
            for vn in fverts:
                fverts2.append(newVerts[vn])
            for uv in obj.fuvs[fn]:
                fuvs2.append(newUvs[uv])
            faceVerts.append(fverts2)
            faceUvs.append(fuvs2)

    weights = {}
    if richMesh.weights:
        for (b, wts1) in list(richMesh.weights.items()):
            wts2 = []
            for (v1,w) in wts1:
                if not killVerts[v1]:
                   wts2.append((newVerts[v1],w))
            weights[b] = wts2

    shapes = []
    if richMesh.shapes:
        for (name, morphs1) in richMesh.shapes:
            morphs2 = {}
            for (v1,dx) in list(morphs1.items()):
                if not killVerts[v1]:
                    morphs2[newVerts[v1]] = dx
            shapes.append((name, morphs2))

    richMesh.fromProxy(coords, texVerts, faceVerts, faceUvs, weights, shapes)
    richMesh.vertexMask = numpy.logical_not(killVerts)
    richMesh.vertexMapping = newVerts
    richMesh.faceMask = numpy.logical_not(faceMask)
    return richMesh


def deleteGroup(name, groups):
    for part in groups:
        if part in name:
            return True
    return False

def getpath(path):
    if isinstance(path, tuple):
        (folder, file) = path
        path = os.path.join(folder, file)
    if path:
        return os.path.realpath(os.path.expanduser(path))
    else:
        return None

def copy(frompath, topath):
    frompath = getpath(frompath)
    if frompath:
        try:
            shutil.copy(frompath, topath)
        except (IOError, os.error) as why:
            log.error("Can't copy %s" % str(why))

