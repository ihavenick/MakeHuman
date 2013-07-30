#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
Handles WaveFront .obj 3D mesh files.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Manuel Bastioni, Marc Flerackers, Jonas Hauquier

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

"""

import os
import module3d
import codecs
import math

def loadObjFile(path, obj = None):
    """
    Parse and load a Wavefront OBJ file as mesh.
    """
    if obj == None:
        name = os.path.splitext( os.path.basename(path) )[0]
        obj = module3d.Object3D(name)

    objFile = open(path)

    fg = None
    mtl = None

    verts = []
    uvs = []
    fverts = []
    fuvs = []
    groups = []
    fmtls = []
    has_uv = False
    materials = {}
    faceGroups = {}

    for objData in objFile:

        lineData = objData.split()
        if len(lineData) > 0:

            command = lineData[0]

            if command == 'v':
                verts.append((float(lineData[1]), float(lineData[2]), float(lineData[3])))

            elif command == 'vt':
                uvs.append((float(lineData[1]), float(lineData[2])))

            elif command == 'f':
                if not fg:
                    if 0 not in faceGroups:
                        faceGroups[0] = obj.createFaceGroup('default-dummy-group')
                    fg = faceGroups[0]

                if mtl is None:
                    if 0 not in materials:
                        materials[0] = obj.createMaterial('')
                    mtl = materials[0]

                uvIndices = []
                vIndices = []
                for faceData in lineData[1:]:
                    vInfo = faceData.split('/')
                    vIdx = int(vInfo[0]) - 1  # -1 because obj is 1 based list
                    vIndices.append(vIdx)

                    # If there are other data (uv, normals, etc)
                    if len(vInfo) > 1 and vInfo[1] != '':
                        uvIndex = int(vInfo[1]) - 1  # -1 because obj is 1 based list
                        uvIndices.append(uvIndex)

                if len(vIndices) == 3:
                    vIndices.append(vIndices[0])
                fverts.append(tuple(vIndices))
                    
                if len(uvIndices) > 0:
                    if len(uvIndices) == 3:
                        uvIndices.append(uvIndices[0])
                    has_uv = True
                if len(uvIndices) < 4:
                    uvIndices = [0, 0, 0, 0]
                fuvs.append(tuple(uvIndices))

                groups.append(fg.idx)
                
                fmtls.append(mtl)

            elif command == 'g':
                fgName = lineData[1]
                if fgName not in faceGroups:
                    faceGroups[fgName] = obj.createFaceGroup(fgName)
                fg =  faceGroups[fgName]

            elif command == 'usemtl':
                mtlName = lineData[1]
                if mtlName not in materials:
                    materials[mtlName] = obj.createMaterial(mtlName)
                mtl =  materials[mtlName]

            elif command == 'o':
                
                obj.name = lineData[1]

    objFile.close()

    obj.setCoords(verts)
    obj.setUVs(uvs)
    obj.setFaces(fverts, fuvs if has_uv else None, groups, fmtls)

    return obj


def writeObjFile(path, objects, writeMTL = True, config = None):
    if not isinstance(objects, list):
        objects = [objects]

    if isinstance(path, file):
        fp = path
    else:
        fp = codecs.open(path, 'w', encoding="utf-8")

    fp.write(
        "# MakeHuman exported OBJ\n" +
        "# www.makehuman.org\n\n")

    if writeMTL:
        mtlfile = path.replace(".obj",".mtl")
        fp.write("mtllib %s\n" % os.path.basename(mtlfile))

    # Vertices
    for obj in objects:
        for co in obj.coord:
            fp.write("v %.4g %.4g %.4g\n" % tuple(co))

    # Vertex normals
    if config == None or config.useNormals:
        for obj in objects:
            obj.calcFaceNormals()
            #obj.calcVertexNormals()
            for no in obj.fnorm:
                no = no/math.sqrt(no.dot(no))
                fp.write("vn %.4g %.4g %.4g\n" % tuple(no))

    # UV vertices
    for obj in objects:
        if obj.has_uv:
            for uv in obj.texco:
                fp.write("vt %.4g %.4g\n" % tuple(uv))

    # Faces
    nVerts = 1
    nTexVerts = 1
    for obj in objects:
        fp.write("usemtl %s\n" % obj.material.name)
        fp.write("g %s\n" % obj.name)
        for fn,fv in enumerate(obj.fvert):
            fp.write('f ')
            fuv = obj.fuvs[fn]
            if fv[0] == fv[3]:
                nv = 3
            else:
                nv = 4
            if config == None or config.useNormals:
                if obj.has_uv:
                    line = []
                    for n in range(nv):
                        vn = fv[n]+nVerts
                        line.append("%d/%d/%d" % (vn, fuv[n]+nTexVerts, fn))
                    fp.write(" ".join(line))
                else:
                    line = []
                    for n in range(nv):
                        vn = fv[n]+nVerts
                        line.append("%d//%d" % (vn, fn))
                    fp.write(" ".join(line))
            else:
                if obj.has_uv:
                    line = []
                    for n in range(nv):
                        vn = fv[n]+nVerts
                        line.append("%d/%d" % (vn, fuv[n]+nTexVerts))
                    fp.write(" ".join(line))
                else:
                    line = []
                    for n in range(nv):
                        vn = fv[n]+nVerts
                        line.append("%d" % (vn))
                    fp.write(" ".join(line))
            fp.write('\n')

        nVerts += len(obj.coord)
        nTexVerts += len(obj.texco)

    fp.close()

    if writeMTL:
        fp = codecs.open(mtlfile, 'w', encoding="utf-8")
        fp.write(
            '# MakeHuman exported MTL\n' +
            '# www.makehuman.org\n\n')
        for obj in objects:
            writeMaterial(fp, obj.material, config)
        fp.close()


#
#   writeMaterial(fp, mat, config):
#

def writeMaterial(fp, mat, texPathConf = None):
    fp.write("\nnewmtl %s\n" % mat.name)
    di = mat.diffuseIntensity
    diff = mat.diffuseColor
    si = mat.specularIntensity
    spec =  mat.specularColor
    fp.write(
        "Kd %.4g %.4g %.4g\n" % (di*diff.r, di*diff.g, di*diff.b) +
        "Ks %.4g %.4g %.4g\n" % (si*spec.r, si*spec.g, si*spec.b) +
        "d %.4g\n" % (1-mat.transparencyIntensity)
    )

    writeTexture(fp, "map_Kd", mat.diffuseTexture, texPathConf)
    writeTexture(fp, "map_Ks", mat.specularMapTexture, texPathConf)
    #writeTexture(fp, "map_Tr", mat.translucencyMapTexture, texPathConf)
    writeTexture(fp, "map_Disp", mat.normalMapTexture, texPathConf)
    writeTexture(fp, "map_Disp", mat.specularMapTexture, texPathConf)
    writeTexture(fp, "map_Disp", mat.displacementMapTexture, texPathConf)

    #import mh
    #writeTexture(fp, "map_Kd", os.path.join(mh.getSysDataPath("textures"), "texture.png"), texPathConf)


def writeTexture(fp, key, filepath, pathConfig = None):
    if not filepath:
        return

    if pathConfig:
        newpath = pathConfig.copyTextureToNewLocation(filepath)
        fp.write("%s %s\n" % (key, newpath))
    else:
        fp.write("%s %s\n" % (key, filepath))

