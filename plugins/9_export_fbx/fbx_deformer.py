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
Fbx mesh
"""

import math
import numpy as np
import numpy.linalg as la
import transformations as tm

from .fbx_utils import *

#--------------------------------------------------------------------
#   Object definitions
#--------------------------------------------------------------------

def getObjectCounts(stuffs):
    nVertexGroups = 0
    for stuff in stuffs:
        for weights in stuff.richMesh.weights:
            if weights:
                nVertexGroups += 1

    nShapes = 0
    for stuff in stuffs:
        for key,shape in stuff.richMesh.shapes:
            if shape:
                nShapes += 1

    return nVertexGroups, nShapes

def countObjects(stuffs, amt):
    nVertexGroups, nShapes = getObjectCounts(stuffs)
    if amt:
        return (nVertexGroups + 1 + 2*nShapes)
    else:
        return 2*nShapes


def writeObjectDefs(fp, stuffs, amt):
    nVertexGroups, nShapes = getObjectCounts(stuffs)

    if amt:
        fp.write(
'    ObjectType: "Deformer" {\n' +
'       Count: %d' % (nVertexGroups + 1 + 2*nShapes) +
"""
    }

    ObjectType: "Pose" {
        Count: 1
    }
""")

    else:
        fp.write(
'    ObjectType: "Deformer" {\n' +
'       Count: %d' % (2*nShapes) +
"""
}
""")


#--------------------------------------------------------------------
#   Object properties
#--------------------------------------------------------------------

def writeObjectProps(fp, stuffs, amt):
    if amt:
        writeBindPose(fp, stuffs, amt)

        for stuff in stuffs:
            name = getStuffName(stuff, amt)
            writeDeformer(fp, name)
            for bone in list(amt.bones.values()):
                try:
                    weights = stuff.richMesh.weights[bone.name]
                except KeyError:
                    continue
                writeSubDeformer(fp, name, bone, weights)

    for stuff in stuffs:
        name = getStuffName(stuff, amt)
        if stuff.richMesh.shapes:
            for sname,shape in stuff.richMesh.shapes:
                writeShapeGeometry(fp, name, sname, shape)
                writeShapeDeformer(fp, name, sname)
                writeShapeSubDeformer(fp, name, sname, shape)


def writeShapeGeometry(fp, name, sname, shape):
        id,key = getId("Geometry::%s_%sShape" % (name, sname))
        nVerts = len(shape)
        fp.write(
'    Geometry: %d, "%s", "Shape" {\n' % (id, key) +
'        version: 100\n' +
'        Indexes: *%d   {\n' % nVerts +
'            a: ')

        last = nVerts - 1
        shape = list(shape.items())
        shape.sort()
        for n,data in enumerate(shape):
            vn,_ = data
            fp.write("%d" % vn)
            writeComma(fp, n, last)

        fp.write(
'        }\n' +
'        Vertices: *%d   {\n' % (3*nVerts) +
'            a: ')

        last = nVerts - 1
        for n,data in enumerate(shape):
            _,dr = data
            fp.write("%.4f,%.4f,%.4f" % tuple(dr))
            writeComma(fp, n, last)

        fp.write(
'        }\n' +
'    }\n')


def writeShapeDeformer(fp, name, sname):
    id,key = getId("Deformer::%s_%sShape" % (name, sname))
    fp.write(
'    Deformer: %d, "%s", "BlendShape" {\n' % (id, key) +
'    }\n')


def writeShapeSubDeformer(fp, name, sname, shape):
    sid,skey = getId("SubDeformer::%s_%sShape" % (name, sname))
    fp.write(
'    Deformer: %d, "%s", "BlendShapeChannel" {' % (sid, skey) +
"""
        version: 100
        deformpercent: 0.0
        FullWeights: *1   {
            a: 100
        }
    }
""")


def writeDeformer(fp, name):
    id,key = getId("Deformer::%s" % name)

    fp.write(
'    Deformer: %d, "%s", "Skin" {' % (id, key) +
"""
        Version: 101
        Properties70:  {
""" +
'            P: "MHName", "KString", "", "", "%sSkin"' % name +
"""
        }
        Link_DeformAcuracy: 50
    }
""")


def writeSubDeformer(fp, name, bone, weights):
    nVertexWeights = len(weights)
    id,key = getId("SubDeformer::%s_%s" % (bone.name, name))

    fp.write(
'    Deformer: %d, "%s", "Cluster" {\n' % (id, key) +
'        Version: 100\n' +
'        UserData: "", ""\n' +
'        Indexes: *%d {\n' % nVertexWeights +
'            a: ')

    last = nVertexWeights - 1
    for n,data in enumerate(weights):
        vn,w = data
        fp.write(str(vn))
        writeComma(fp, n, last)

    fp.write(
'        } \n' +
'        Weights: *%d {\n' % nVertexWeights +
'            a: ')

    for n,data in enumerate(weights):
        vn,w = data
        fp.write(str(w))
        writeComma(fp, n, last)

    fp.write('        }\n')
    writeMatrix(fp, 'Transform', bone.bindMatrix)
    writeMatrix(fp, 'TransformLink', bone.bindInverse)
    fp.write('    }\n')


def writeBindPose(fp, stuffs, amt):
    id,key = getId("Pose::" + amt.name)
    nBones = len(amt.bones)
    nMeshes = len(stuffs)

    fp.write(
'    Pose: %d, "%s", "BindPose" {\n' % (id, key)+
'        Type: "BindPose"\n' +
'        Version: 100\n' +
'        NbPoseNodes: %d\n' % (1+nMeshes+nBones))

    startLinking()
    poseNode(fp, "Model::%s" % amt.name, amt.bindMatrix)

    for stuff in stuffs:
        name = getStuffName(stuff, amt)
        poseNode(fp, "Model::%sMesh" % name, amt.bindMatrix)

    for bone in list(amt.bones.values()):
        poseNode(fp, "Model::%s" % bone.name, bone.bindMatrix)

    stopLinking()
    fp.write('    }\n')


def poseNode(fp, key, matrix):
    pid,_ = getId(key)
    matrix[:3,3] = 0
    fp.write(
'        PoseNode:  {\n' +
'            Node: %d\n' % pid)
    writeMatrix(fp, 'Matrix', matrix, "    ")
    fp.write('        }\n')

#--------------------------------------------------------------------
#   Links
#--------------------------------------------------------------------

def writeLinks(fp, stuffs, amt):

    if amt:
        for stuff in stuffs:
            name = getStuffName(stuff, amt)

            ooLink(fp, 'Deformer::%s' % name, 'Geometry::%s' % name)
            for bone in list(amt.bones.values()):
                subdef = 'SubDeformer::%s_%s' % (bone.name, name)
                try:
                    getId(subdef)
                except NameError:
                    continue
                ooLink(fp, subdef, 'Deformer::%s' % name)
                ooLink(fp, 'Model::%s' % bone.name, subdef)

    for stuff in stuffs:
        if stuff.richMesh.shapes:
            name = getStuffName(stuff, amt)
            for sname, shape in stuff.richMesh.shapes:
                deform = "Deformer::%s_%sShape" % (name, sname)
                subdef = "SubDeformer::%s_%sShape" % (name, sname)
                ooLink(fp, "Geometry::%s_%sShape" % (name, sname), subdef)
                ooLink(fp, subdef, deform)
                ooLink(fp, deform, "Geometry::%s" % name)


