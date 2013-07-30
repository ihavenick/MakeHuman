#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson, Jonas Hauquier

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

MakeHuman to Collada (MakeHuman eXchange format) exporter. Collada files can be loaded into
Blender by collada_import.py.

TODO
"""

import os.path
import time
import codecs
import math
import numpy as np
import transformations as tm
import log

import gui3d
import exportutils
import posemode

#
#    Size of end bones = 1 mm
#
Delta = [0,0.01,0]


#
# exportCollada(human, filepath, config):
#

def exportCollada(human, filepath, config):
    #posemode.exitPoseMode()
    #posemode.enterPoseMode()
    gui3d.app.progress(0, text="Preparing")

    time1 = time.clock()
    config.setHuman(human)
    config.setupTexFolder(filepath)
    filename = os.path.basename(filepath)
    name = config.goodName(os.path.splitext(filename)[0])

    rawTargets = exportutils.collect.readTargets(human, config)
    rmeshes,amt = exportutils.collect.setupObjects(
        name,
        human,
        config=config,
        rawTargets = rawTargets,
        helpers=config.helpers,
        eyebrows=config.eyebrows,
        lashes=config.lashes)

    amt.calcBindMatrices()

    gui3d.app.progress(0.5, text="Exporting %s" % filepath)

    try:
        fp = codecs.open(filepath, 'w', encoding="utf-8")
        log.message("Writing Collada file %s" % filepath)
    except:
        log.error("Unable to open file for writing %s" % filepath)

    date = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())
    fp.write('<?xml version="1.0" encoding="utf-8"?>\n' +
        '<COLLADA version="1.4.0" xmlns="http://www.collada.org/2005/11/COLLADASchema">\n' +
        '  <asset>\n' +
        '    <contributor>\n' +
        '      <author>www.makehuman.org</author>\n' +
        '    </contributor>\n' +
        '    <created>%s</created>\n' % date +
        '    <modified>%s</modified>\n' % date +
        '    <unit meter="1.0" name="meter"/>\n' +
        '    <up_axis>Y_UP</up_axis>\n' +
        '  </asset>\n' +
        '  <library_images>\n')

    for rmesh in rmeshes:
        writeImages(fp, rmesh, config)

    fp.write(
        '  </library_images>\n' +
        '  <library_effects>\n')

    gui3d.app.progress(0.1, text="Exporting effects")
    for rmesh in rmeshes:
        writeEffects(fp, rmesh)

    fp.write(
        '  </library_effects>\n' +
        '  <library_materials>\n')

    gui3d.app.progress(0.2, text="Exporting materials")
    for rmesh in rmeshes:
        writeMaterials(fp, rmesh)

    fp.write(
        '  </library_materials>\n'+
        '  <library_controllers>\n')

    gui3d.app.progress(0.3, text="Exporting controllers")
    for rmesh in rmeshes:
        writeController(fp, rmesh, amt, config)

    fp.write(
        '  </library_controllers>\n'+
        '  <library_geometries>\n')

    dt = 0.4/len(rmeshes)
    t = 0.4
    for rmesh in rmeshes:
        gui3d.app.progress(t, text="Exporting %s" % rmesh.name)
        t += dt
        writeGeometry(fp, rmesh, config)

    gui3d.app.progress(0.8, text="Exporting bones")
    fp.write(
        '  </library_geometries>\n\n' +
        '  <library_visual_scenes>\n' +
        '    <visual_scene id="Scene" name="Scene">\n' +
        '      <node id="%s">\n' % name +
        '        <matrix sid="transform">\n')


    if config.rotate90X:
        mat = tm.rotation_matrix(-math.pi/2, (1,0,0))
    else:
        mat = np.identity(4, float)
    if config.rotate90Z:
        rotZ = tm.rotation_matrix(math.pi/2, (0,0,1))
        mat = np.dot(mat, rotZ)
    for i in range(4):
        fp.write('          %.4f %.4f %.4f %.4f\n' % (mat[i][0], mat[i][1], mat[i][2], mat[i][3]))

    fp.write('        </matrix>\n')

    for root in amt.hierarchy:
        writeBone(fp, root, [0,0,0], 'layer="L1"', '    ', amt, config)

    gui3d.app.progress(0.9, text="Exporting nodes")
    for rmesh in rmeshes:
        writeNode(fp, "        ", rmesh, amt, config)

    fp.write(
        '      </node>\n' +
        '    </visual_scene>\n' +
        '  </library_visual_scenes>\n' +
        '  <scene>\n' +
        '    <instance_visual_scene url="#Scene"/>\n' +
        '  </scene>\n' +
        '</COLLADA>\n')

    fp.close()
    time2 = time.clock()
    log.message("Wrote Collada file in %g s: %s" % (time2-time1, filepath))
    gui3d.app.progress(1)
    #posemode.exitPoseMode()
    return

#
#   Write images
#

def writeImages(fp, rmesh, config):
    mat = rmesh.material
    if mat.diffuseTexture:
        writeImage(fp, mat.diffuseTexture, config)
    if mat.specularMapTexture:
        writeImage(fp, mat.specularMapTexture, config)
    if mat.bumpMapTexture:
        writeImage(fp, mat.bumpMapTexture, config)
    if mat.normalMapTexture:
        writeImage(fp, mat.normalMapTexture, config)
    if mat.displacementMapTexture:
        writeImage(fp, mat.displacementMapTexture, config)


def getTextureName(filepath):
    texfile = os.path.basename(filepath)
    return texfile.replace(".","_")


def writeImage(fp, filepath, config):
    if not filepath:
        return
    newpath = config.copyTextureToNewLocation(filepath)
    print "Collada Image", filepath, newpath
    texname = getTextureName(filepath)
    fp.write(
        '    <image id="%s" name="%s">\n' % (texname, texname) +
        '      <init_from>%s</init_from>\n' % newpath +
        '    </image>\n'
    )

#
#    writeEffects(fp, rmesh):
#

def writeIntensity(fp, tech, intensity):
    fp.write('            <%s><float>%s</float></%s>\n' % (tech, intensity, tech))


def writeTexture(fp, tech, filepath, color, intensity, s=1.0):
    if not filepath:
        return

    fp.write('            <%s>\n' % tech)
    if color:
        fp.write('            <color>%.4f %.4f %.4f 1</color> \n' % (s*color.r, s*color.g, s*color.b))
    if intensity:
        fp.write('            <float>%s</float>\n' % intensity)
    texname = getTextureName(filepath)
    fp.write(
        '              <texture texture="%s-sampler" texcoord="UVTex"/>\n' % texname +
        '            </%s>\n' % tech)


def writeEffects(fp, rmesh):
    mat = rmesh.material
    fp.write(
       '    <effect id="%s-effect">\n' % mat.name.replace(" ", "_") +
       '      <profile_COMMON>\n')

    writeSurfaceSampler(fp, mat.diffuseTexture)
    writeSurfaceSampler(fp, mat.specularMapTexture)
    writeSurfaceSampler(fp, mat.normalMapTexture)
    writeSurfaceSampler(fp, mat.bumpMapTexture)
    writeSurfaceSampler(fp, mat.displacementMapTexture)

    fp.write(
        '        <technique sid="common">\n' +
        '          <phong>\n')

    writeTexture(fp, 'diffuse', mat.diffuseTexture, mat.diffuseColor, mat.diffuseIntensity)
    writeTexture(fp, 'transparency', mat.diffuseTexture, None, mat.transparencyIntensity)
    writeTexture(fp, 'specular', mat.specularMapTexture, mat.specularColor, 0.1*mat.specularIntensity)
    writeIntensity(fp, 'shininess', mat.specularHardness)
    writeTexture(fp, 'normal', mat.normalMapTexture, None, mat.normalMapIntensity)
    writeTexture(fp, 'bump', mat.bumpMapTexture, None, mat.bumpMapIntensity)
    writeTexture(fp, 'displacement', mat.displacementMapTexture, None, mat.displacementMapIntensity)

    fp.write(
        '          </phong>\n' +
        '          <extra/>\n' +
        '        </technique>\n' +
        '        <extra>\n' +
        '          <technique profile="GOOGLEEARTH">\n' +
        '            <show_double_sided>1</show_double_sided>\n' +
        '          </technique>\n' +
        '        </extra>\n' +
        '      </profile_COMMON>\n' +
        '      <extra><technique profile="MAX3D"><double_sided>1</double_sided></technique></extra>\n' +
        '    </effect>\n')


def writeSurfaceSampler(fp, filepath):
    if not filepath:
        return
    texname = getTextureName(filepath)
    fp.write(
        '        <newparam sid="%s-surface">\n' % texname +
        '          <surface type="2D">\n' +
        '            <init_from>%s</init_from>\n' % texname +
        '          </surface>\n' +
        '        </newparam>\n' +
        '        <newparam sid="%s-sampler">\n' % texname +
        '          <sampler2D>\n' +
        '            <source>%s-surface</source>\n' % texname +
        '          </sampler2D>\n' +
        '        </newparam>\n')

#
#    writeMaterials(fp, rmesh):
#

def writeMaterials(fp, rmesh):
    mat = rmesh.material
    matname = mat.name.replace(" ", "_")
    fp.write(
        '    <material id="%s" name="%s">\n' % (matname, matname) +
        '      <instance_effect url="#%s-effect"/>\n' % matname +
        '    </material>\n')


def writeController(fp, rmesh, amt, config):
    obj = rmesh.object
    rmesh.calculateSkinWeights(amt)
    nVerts = len(obj.coord)
    nUvVerts = len(obj.texco)
    nFaces = len(obj.fvert)
    nWeights = len(rmesh.skinWeights)
    nBones = len(amt.bones)
    nShapes = len(rmesh.shapes)

    fp.write('\n' +
        '    <controller id="%s-skin">\n' % rmesh.name +
        '      <skin source="#%sMesh">\n' % rmesh.name +
        '        <bind_shape_matrix>\n' +
        '          1 0 0 0 \n' +
        '          0 0 -1 0 \n' +
        '          0 1 0 0 \n' +
        '          0 0 0 1 \n' +
        '        </bind_shape_matrix>\n' +
        '        <source id="%s-skin-joints">\n' % rmesh.name +
        '          <IDREF_array count="%d" id="%s-skin-joints-array">\n' % (nBones,rmesh.name) +
        '           ')

    for bone in amt.bones.values():
        fp.write(' %s' % bone.name)

    fp.write('\n' +
        '          </IDREF_array>\n' +
        '          <technique_common>\n' +
        '            <accessor count="%d" source="#%s-skin-joints-array" stride="1">\n' % (nBones,rmesh.name) +
        '              <param type="IDREF" name="JOINT"></param>\n' +
        '            </accessor>\n' +
        '          </technique_common>\n' +
        '        </source>\n' +
        '        <source id="%s-skin-weights">\n' % rmesh.name +
        '          <float_array count="%d" id="%s-skin-weights-array">\n' % (nWeights,rmesh.name) +
        '           ')

    for w in rmesh.skinWeights:
        fp.write(' %s' % w[1])

    fp.write('\n' +
        '          </float_array>\n' +
        '          <technique_common>\n' +
        '            <accessor count="%d" source="#%s-skin-weights-array" stride="1">\n' % (nWeights,rmesh.name) +
        '              <param type="float" name="WEIGHT"></param>\n' +
        '            </accessor>\n' +
        '          </technique_common>\n' +
        '        </source>\n' +
        '        <source id="%s-skin-poses">\n' % rmesh.name +
        '          <float_array count="%d" id="%s-skin-poses-array">' % (16*nBones,rmesh.name))


    """
    mat = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
    for bone in amt.bones.values():
        (x,y,z) = rotateLoc(bone.head, config)
        mat[0][3] = -x
        mat[1][3] = -y
        mat[2][3] = -z
        fp.write('\n            ')
        for i in range(4):
            for j in range(4):
                fp.write('%.4f ' % mat[i][j])

    """

    for bone in amt.bones.values():
        #bone.calcBindMatrix()
        mat = bone.bindMatrix
        mat = bone.getBindMatrixCollada()
        for i in range(4):
            fp.write('\n           ')
            for j in range(4):
                fp.write(' %.4f' % mat[i,j])
        fp.write('\n')

    fp.write('\n' +
        '          </float_array>\n' +
        '          <technique_common>\n' +
        '            <accessor count="%d" source="#%s-skin-poses-array" stride="16">\n' % (nBones,rmesh.name) +
        '              <param type="float4x4"></param>\n' +
        '            </accessor>\n' +
        '          </technique_common>\n' +
        '        </source>\n' +
        '        <joints>\n' +
        '          <input semantic="JOINT" source="#%s-skin-joints"/>\n' % rmesh.name +
        '          <input semantic="INV_BIND_MATRIX" source="#%s-skin-poses"/>\n' % rmesh.name +
        '        </joints>\n' +
        '        <vertex_weights count="%d">\n' % nVerts +
        '          <input offset="0" semantic="JOINT" source="#%s-skin-joints"/>\n' % rmesh.name +
        '          <input offset="1" semantic="WEIGHT" source="#%s-skin-weights"/>\n' % rmesh.name +
        '          <vcount>\n' +
        '            ')

    for wts in rmesh.vertexWeights:
        fp.write('%d ' % len(wts))

    fp.write('\n' +
        '          </vcount>\n'
        '          <v>\n' +
        '           ')

    for wts in rmesh.vertexWeights:
        for pair in wts:
            fp.write(' %d %d' % pair)

    fp.write('\n' +
        '          </v>\n' +
        '        </vertex_weights>\n' +
        '      </skin>\n' +
        '    </controller>\n')

    # Morph controller

    if rmesh.shapes:
        nShapes = len(rmesh.shapes)

        fp.write(
            '    <controller id="%sMorph" name="%sMorph">\n' % (rmesh.name, rmesh.name)+
            '      <morph source="#%sMesh" method="NORMALIZED">\n' % (rmesh.name) +
            '        <source id="%sTargets">\n' % (rmesh.name) +
            '          <IDREF_array id="%sTargets-array" count="%d">' % (rmesh.name, nShapes))

        for key,_ in rmesh.shapes:
            fp.write(" %sMeshMorph_%s" % (rmesh.name, key))

        fp.write(
            '        </IDREF_array>\n' +
            '          <technique_common>\n' +
            '            <accessor source="#%sTargets-array" count="%d" stride="1">\n' % (rmesh.name, nShapes) +
            '              <param name="IDREF" type="IDREF"/>\n' +
            '            </accessor>\n' +
            '          </technique_common>\n' +
            '        </source>\n' +
            '        <source id="%sWeights">\n' % (rmesh.name) +
            '          <float_array id="%sWeights-array" count="%d">' % (rmesh.name, nShapes))

        fp.write(nShapes*" 0")

        fp.write('\n' +
            '        </float_array>\n' +
            '          <technique_common>\n' +
            '            <accessor source="#%sWeights-array" count="%d" stride="1">\n' % (rmesh.name, nShapes) +
            '              <param name="MORPH_WEIGHT" type="float"/>\n' +
            '            </accessor>\n' +
            '          </technique_common>\n' +
            '        </source>\n' +
            '        <targets>\n' +
            '          <input semantic="MORPH_TARGET" source="#%sTargets"/>\n' % (rmesh.name) +
            '          <input semantic="MORPH_WEIGHT" source="#%sWeights"/>\n' % (rmesh.name) +
            '        </targets>\n' +
            '      </morph>\n' +
            '    </controller>\n')



#
#    writeGeometry(fp, rmesh, config):
#

def writeGeometry(fp, rmesh, config):
    obj = rmesh.object
    nVerts = len(obj.coord)
    nUvVerts = len(obj.texco)
    nWeights = len(rmesh.skinWeights)
    nShapes = len(rmesh.shapes)

    fp.write('\n' +
        '    <geometry id="%sMesh" name="%s">\n' % (rmesh.name,rmesh.name) +
        '      <mesh>\n' +
        '        <source id="%s-Position">\n' % rmesh.name +
        '          <float_array count="%d" id="%s-Position-array">\n' % (3*nVerts,rmesh.name) +
        '          ')


    for co in obj.coord:
        (x,y,z) = rotateLoc(co, config)
        fp.write("%.4f %.4f %.4f " % (x,y,z))

    fp.write('\n' +
        '          </float_array>\n' +
        '          <technique_common>\n' +
        '            <accessor count="%d" source="#%s-Position-array" stride="3">\n' % (nVerts,rmesh.name) +
        '              <param type="float" name="X"></param>\n' +
        '              <param type="float" name="Y"></param>\n' +
        '              <param type="float" name="Z"></param>\n' +
        '            </accessor>\n' +
        '          </technique_common>\n' +
        '        </source>\n')

    # Normals

    if config.useNormals:
        obj.calcFaceNormals()
        nNormals = len(obj.fnorm)
        fp.write(
            '        <source id="%s-Normals">\n' % rmesh.name +
            '          <float_array count="%d" id="%s-Normals-array">\n' % (3*nNormals,rmesh.name) +
            '          ')

        for no in obj.fnorm:
            (x,y,z) = rotateLoc(no, config)
            fp.write("%.4f %.4f %.4f " % (x,y,z))

        fp.write('\n' +
            '          </float_array>\n' +
            '          <technique_common>\n' +
            '            <accessor count="%d" source="#%s-Normals-array" stride="3">\n' % (nNormals,rmesh.name) +
            '              <param type="float" name="X"></param>\n' +
            '              <param type="float" name="Y"></param>\n' +
            '              <param type="float" name="Z"></param>\n' +
            '            </accessor>\n' +
            '          </technique_common>\n' +
            '        </source>\n')

    # UV coordinates

    fp.write(
        '        <source id="%s-UV">\n' % rmesh.name +
        '          <float_array count="%d" id="%s-UV-array">\n' % (2*nUvVerts,rmesh.name) +
        '           ')


    for uv in obj.texco:
        fp.write(" %.4f %.4f" % tuple(uv))

    fp.write('\n' +
        '          </float_array>\n' +
        '          <technique_common>\n' +
        '            <accessor count="%d" source="#%s-UV-array" stride="2">\n' % (nUvVerts,rmesh.name) +
        '              <param type="float" name="S"></param>\n' +
        '              <param type="float" name="T"></param>\n' +
        '            </accessor>\n' +
        '          </technique_common>\n' +
        '        </source>\n')

    # Faces

    fp.write(
        '        <vertices id="%s-Vertex">\n' % rmesh.name +
        '          <input semantic="POSITION" source="#%s-Position"/>\n' % rmesh.name +
        '        </vertices>\n')

    checkFaces(rmesh, nVerts, nUvVerts)
    #writePolygons(fp, rmesh, config)
    writePolylist(fp, rmesh, config)

    fp.write(
        '      </mesh>\n' +
        '    </geometry>\n')

    for name,shape in rmesh.shapes:
        writeShapeKey(fp, name, shape, rmesh, config)
    return


def writeShapeKey(fp, name, shape, rmesh, config):
    obj = rmesh.object
    nVerts = len(obj.coord)

    # Verts

    fp.write(
        '    <geometry id="%sMeshMorph_%s" name="%s">\n' % (rmesh.name, name, name) +
        '      <mesh>\n' +
        '        <source id="%sMeshMorph_%s-positions">\n' % (rmesh.name, name) +
        '          <float_array id="%sMeshMorph_%s-positions-array" count="%d">\n' % (rmesh.name, name, 3*nVerts) +
        '           ')

    target = np.array(obj.coord)
    for n,dr in shape.items():
        target[n] += np.array(dr)
    for co in target:
        loc = rotateLoc(co, config)
        fp.write(" %.4g %.4g %.4g" % tuple(loc))

    fp.write('\n' +
        '          </float_array>\n' +
        '          <technique_common>\n' +
        '            <accessor source="#%sMeshMorph_%s-positions-array" count="%d" stride="3">\n' % (rmesh.name, name, nVerts) +
        '              <param name="X" type="float"/>\n' +
        '              <param name="Y" type="float"/>\n' +
        '              <param name="Z" type="float"/>\n' +
        '            </accessor>\n' +
        '          </technique_common>\n' +
        '        </source>\n')

    # Normals
    """
    fp.write(
'        <source id="%sMeshMorph_%s-normals">\n' % (rmesh.name, name) +
'          <float_array id="%sMeshMorph_%s-normals-array" count="18">\n' % (rmesh.name, name))
-0.9438583 0 0.3303504 0 0.9438583 0.3303504 0.9438583 0 0.3303504 0 -0.9438583 0.3303504 0 0 -1 0 0 1
    fp.write(
        '          </float_array>\n' +
        '          <technique_common>\n' +
        '            <accessor source="#%sMeshMorph_%s-normals-array" count="6" stride="3">\n' % (rmesh.name, name) +
        '              <param name="X" type="float"/>\n' +
        '              <param name="Y" type="float"/>\n' +
        '              <param name="Z" type="float"/>\n' +
        '            </accessor>\n' +
        '          </technique_common>\n' +
        '        </source>\n')
    """

    # Polylist

    fp.write(
        '        <vertices id="%sMeshMorph_%s-vertices">\n' % (rmesh.name, name) +
        '          <input semantic="POSITION" source="#%sMeshMorph_%s-positions"/>\n' % (rmesh.name, name) +
        '        </vertices>\n' +
        '        <polylist count="%d">\n' % len(obj.fvert) +
        '          <input semantic="VERTEX" source="#%sMeshMorph_%s-vertices" offset="0"/>\n' % (rmesh.name, name) +
        #'          <input semantic="NORMAL" source="#%sMeshMorph_%s-normals" offset="1"/>\n' % (rmesh.name, name) +
        '          <vcount>')

    for fv in obj.fvert:
        if fv[0] == fv[3]:
            fp.write("3 ")
        else:
            fp.write("4 ")

    fp.write('\n' +
        '          </vcount>\n' +
        '          <p>')

    for fv in obj.fvert:
        if fv[0] == fv[3]:
            fp.write("%d %d %d " % (fv[0], fv[1], fv[2]))
        else:
            fp.write("%d %d %d %s " % (fv[0], fv[1], fv[2], fv[3]))

    fp.write('\n' +
        '          </p>\n' +
        '        </polylist>\n' +
        '      </mesh>\n' +
        '    </geometry>\n')


#
#   writePolygons(fp, rmesh, config):
#   writePolylist(fp, rmesh, config):
#

def writePolygons(fp, rmesh, config):
    obj = rmesh.object
    fp.write(
        '        <polygons count="%d">\n' % len(obj.fvert) +
        '          <input offset="0" semantic="VERTEX" source="#%s-Vertex"/>\n' % rmesh.name +
        '          <input offset="1" semantic="NORMAL" source="#%s-Normals"/>\n' % rmesh.name +
        '          <input offset="2" semantic="TEXCOORD" source="#%s-UV"/>\n' % rmesh.name)

    for fn,fverts in enumerate(obj.fvert):
        fuv = obj.fuvs[fn]
        fp.write('          <p>')
        for n,vn in enumerate(fverts):
            fp.write("%d %d %d " % (vn, vn, fuv[n]))
        fp.write('</p>\n')

    fp.write('\n' +
        '        </polygons>\n')
    return

def writePolylist(fp, rmesh, config):
    obj = rmesh.object
    fp.write(
        '        <polylist count="%d">\n' % len(obj.fvert) +
        '          <input offset="0" semantic="VERTEX" source="#%s-Vertex"/>\n' % rmesh.name)

    if config.useNormals:
        fp.write(
        '          <input offset="1" semantic="NORMAL" source="#%s-Normals"/>\n' % rmesh.name +
        '          <input offset="2" semantic="TEXCOORD" source="#%s-UV"/>\n' % rmesh.name +
        '          <vcount>')
    else:
        fp.write(
        '          <input offset="1" semantic="TEXCOORD" source="#%s-UV"/>\n' % rmesh.name +
        '          <vcount>')

    for fv in obj.fvert:
        if fv[0] == fv[3]:
            fp.write('3 ')
        else:
            fp.write('4 ')

    fp.write('\n' +
        '          </vcount>\n'
        '          <p>')

    for fn,fv in enumerate(obj.fvert):
        fuv = obj.fuvs[fn]
        if fv[0] == fv[3]:
            nverts = 3
        else:
            nverts = 4
        if config.useNormals:
            for n in range(nverts):
                fp.write("%d %d %d " % (fv[n], fn, fuv[n]))
        else:
            for n in range(nverts):
                fp.write("%d %d " % (fv[n], fuv[n]))

    fp.write(
        '          </p>\n' +
        '        </polylist>\n')
    return

#
#   checkFaces(rmesh, nVerts, nUvVerts):
#

def checkFaces(rmesh, nVerts, nUvVerts):
    obj = rmesh.object
    for fn,fverts in enumerate(obj.fvert):
        for n,vn in enumerate(fverts):
            uv = obj.fuvs[fn][n]
            if vn > nVerts:
                raise NameError("v %d > %d" % (vn, nVerts))
            if uv > nUvVerts:
                raise NameError("uv %d > %d" % (uv, nUvVerts))
    return


def writeNode(fp, pad, rmesh, amt, config):

    fp.write('\n' +
        '%s<node id="%sObject" name="%s">\n' % (pad, rmesh.name,rmesh.name) +
        '%s  <matrix sid="transform">\n' % pad +
        '%s    1 0 0 0\n' % pad +
        '%s    0 1 0 0\n' % pad +
        '%s    0 0 1 0\n' % pad +
        '%s    0 0 0 1\n' % pad +
        '%s  </matrix>\n' % pad +
        '%s  <instance_controller url="#%s-skin">\n' % (pad, rmesh.name) +
        '%s    <skeleton>#%sSkeleton</skeleton>\n' % (pad, amt.roots[0].name))

    mat = rmesh.material
    matname = mat.name.replace(" ", "_")
    fp.write(
        '%s    <bind_material>\n' % pad +
        '%s      <technique_common>\n' % pad +
        '%s        <instance_material symbol="%s" target="#%s">\n' % (pad, matname, matname) +
        '%s          <bind_vertex_input semantic="UVTex" input_semantic="TEXCOORD" input_set="0"/>\n' % pad +
        '%s        </instance_material>\n' % pad +
        '%s      </technique_common>\n' % pad +
        '%s    </bind_material>\n' % pad)

    fp.write(
        '%s  </instance_controller>\n' % pad +
        '%s</node>\n' % pad)
    return


def rotateLoc(loc, config):
    return loc
    (x,y,z) = loc
    if config.rotate90X:
        yy = -z
        z = y
        y = yy
    if config.rotate90Z:
        yy = x
        x = -y
        y = yy
    return (x,y,z)


def writeBone(fp, hier, orig, extra, pad, amt, config):
    (bone, children) = hier
    if bone:
        nameStr = 'sid="%s"' % bone.name
        idStr = 'id="%s" name="%s"' % (bone.name, bone.name)
    else:
        nameStr = ''
        idStr = ''

    fp.write(
        '%s      <node %s %s type="JOINT" %s>\n' % (pad, extra, nameStr, idStr) +
        '%s        <matrix sid="transform">\n' % pad)
    mat = bone.matrixRelative
    for i in range(4):
        fp.write('%s          %.5f %.5f %.5f %.5f\n' % (pad, mat[i][0], mat[i][1], mat[i][2], mat[i][3]))
    fp.write('%s        </matrix>\n' % pad)

    for child in children:
        writeBone(fp, child, bone.head, '', pad+'  ', amt, config)

    fp.write('%s      </node>\n' % pad)
    return


