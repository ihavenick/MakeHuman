#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makeinfo.human.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makeinfo.human.org/node/318)

**Coding Standards:**  See http://www.makeinfo.human.org/node/165

Abstract
--------

Proxies
"""

import os
import log
import gui3d

from . import mhx_mesh
from . import mhx_materials

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------

def writeProxyType(type, test, env, fp, t0, t1):
    n = 0
    for proxy in env.proxies.values():
        if proxy.type == type:
            n += 1
    if n == 0:
        return

    dt = (t1-t0)/n
    t = t0
    for proxy in env.proxies.values():
        if proxy.type == type:
            gui3d.app.progress(t, text="Exporting %s" % proxy.name)
            fp.write("#if toggle&%s\n" % test)
            writeProxy(fp, env, proxy)
            fp.write("#endif\n")
            t += dt


#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------

def writeProxy(fp, env, proxy):
    scale = env.config.scale

    fp.write("""
NoScale False ;
""")

    # Proxy material

    writeProxyMaterial(fp, proxy, env)

    # Proxy mesh

    name = env.name + proxy.name
    fp.write(
        "Mesh %sMesh %sMesh \n" % (name, name) +
        "  Verts\n")

    amt = env.armature
    ox = amt.origin[0]
    oy = amt.origin[1]
    oz = amt.origin[2]
    for x,y,z in proxy.getCoords():
        fp.write("  v %.4f %.4f %.4f ;\n" % (scale*(x-ox), scale*(-z+oz), scale*(y-oy)))

    fp.write("""
  end Verts
  Faces
""")

    obj = proxy.getObject()
    for fv in obj.fvert:
        fp.write("    f %d %d %d %d ;\n" % (fv[0], fv[1], fv[2], fv[3]))
    #if False and proxy.faceNumbers:
    #    for ftn in proxy.faceNumbers:
    #        fp.write(ftn)
    #else:
    fp.write("    ftall 0 1 ;\n")

    fp.write("  end Faces\n")

    # Proxy layers

    fp.write(
        "  MeshTextureFaceLayer %s\n" % "Texture" +
        "    Data \n")
    for fuv in obj.fuvs:
        fp.write("    vt")
        for vt in fuv:
            uv = obj.texco[vt]
            fp.write(" %.4g %.4g" % tuple(uv))
        fp.write(" ;\n")
    fp.write(
        "    end Data\n" +
        "  end MeshTextureFaceLayer\n")

    '''
    #Support for multiple texture layers currently disabled.

    layers = list( proxy.uvtexLayerName.keys())
    list.sort()
    for layer in layers:
        if layer == proxy.objFileLayer
            continue
        try:
            texfaces = proxy.texFacesLayers[layer]
            texverts = proxy.texVertsLayers[layer]
        except KeyError:
            continue
        fp.write(
            "  MeshTextureFaceLayer %s\n" % proxy.uvtexLayerName[layer] +
            "    Data \n")

        if layer == proxy.objFileLayer:
            for fuv in obj.fuvs:
                fp.write("    vt")
                for vt in fuv:
                    uv = obj.texco[vt]
                    fp.write(" %.4g %.4g" % (uv[0], uv[1]))
                fp.write(" ;\n")
        else:
            pass

        fp.write(
            "    end Data\n" +
            "  end MeshTextureFaceLayer\n")
    '''

    # Proxy vertex groups

    mhx_mesh.writeVertexGroups(fp, env, proxy)

    if proxy.useBaseMaterials:
        mhx_mesh.writeBaseMaterials(fp, env)
    elif proxy.material:
        fp.write("  Material %s_%s_%s ;" % (env.name, proxy.name, proxy.material.name))


    fp.write("""
end Mesh
""")

    # Proxy object

    name = env.name + proxy.name
    fp.write(
        "Object %sMesh MESH %sMesh \n" % (name, name) +
        "  parent Refer Object %s ;\n" % env.name +
        "  hide False ;\n" +
        "  hide_render False ;\n")
    if proxy.wire:
        fp.write("  draw_type 'WIRE' ;\n")


    # Proxy layers

    fp.write("layers Array ")
    for n in range(20):
        if n == proxy.layer:
            fp.write("1 ")
        else:
            fp.write("0 ")
    fp.write(";\n")

    fp.write("""
#if toggle&T_Armature
""")

    mhx_mesh.writeArmatureModifier(fp, env, proxy)
    writeProxyModifiers(fp, env, proxy)

    fp.write("""
  parent_type 'OBJECT' ;
#endif
  color Array 1.0 1.0 1.0 1.0  ;
  show_name True ;
  select True ;
  lock_location Array 1 1 1 ;
  lock_rotation Array 1 1 1 ;
  lock_scale Array 1 1 1  ;
  Property MhxScale theScale ;
  Property MhxProxy True ;
end Object
""")

    mhx_mesh.writeHideAnimationData(fp, env, env.name, proxy.name)

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------

def writeProxyModifiers(fp, env, proxy):
    for mod in proxy.modifiers:
        if mod[0] == 'subsurf':
            fp.write(
                "    Modifier SubSurf SUBSURF\n" +
                "      levels %d ;\n" % mod[1] +
                "      render_levels %d ;\n" % mod[2] +
                "    end Modifier\n")
        elif mod[0] == 'shrinkwrap':
            offset = mod[1]
            fp.write(
                "    Modifier ShrinkWrap SHRINKWRAP\n" +
                "      target Refer Object %sMesh ;\n" % env.name +
                "      offset %.4f ;\n" % offset +
                "      use_keep_above_surface True ;\n" +
                "    end Modifier\n")
        elif mod[0] == 'solidify':
            thickness = mod[1]
            offset = mod[2]
            fp.write(
                "    Modifier Solidify SOLIDIFY\n" +
                "      thickness %.4f ;\n" % thickness +
                "      offset %.4f ;\n" % offset +
                "    end Modifier\n")
    return


def writeProxyMaterial(fp, proxy, env):
    mat = proxy.material

    if mat.diffuseTexture:
        mat.diffuseTexture = proxy.getActualTexture(env.human)
        alpha = 0
    else:
        alpha = 1 - mat.transparencyIntensity

    prefix = env.name+"_"+proxy.name
    texnames = mhx_materials.writeTextures(fp, mat, prefix, env)

    # Write materials

    prxList = sortedMasks(env)
    nMasks = countMasks(proxy, prxList)
    nMasks = 0

    fp.write("Material %s_%s_%s \n" % (env.name, proxy.name, mat.name))
    #addProxyMaskMTexs(fp, mat, proxy, prxList)
    #uvlayer = proxy.uvtexLayerName[proxy.textureLayer]
    uvlayer = "Texture"

    mhx_materials.writeMTexes(fp, texnames, mat, nMasks, env)
    mhx_materials.writeMaterialSettings(fp, mat, alpha, env)

    fp.write(
        "  Property MhxDriven True ;\n" +
        "end Material\n\n")


def addProxyMaskMTexs(fp, mat, proxy, prxList):
    if proxy.maskLayer < 0:
        return
    n = 0
    m = len(prxList)
    for (zdepth, prx) in prxList:
        m -= 1
        if zdepth > proxy.z_depth:
            n = mhx_materials.addMaskMTex(fp, prx.mask, proxy, 'MULTIPLY', n)
    if True or not tex:
        n = mhx_materials.addMaskMTex(fp, 'solid', proxy, 'MIX', n)


def sortedMasks(env):
    if not env.config.useMasks:
        return []
    prxList = []
    for prx in env.proxies.values():
        if prx.type == 'Clothes' and prx.mask:
            prxList.append((prx.z_depth, prx))
    prxList.sort()
    return prxList


def countMasks(proxy, prxList):
    n = 0
    for (zdepth, prx) in prxList:
        if prx.type == 'Clothes' and zdepth > proxy.z_depth:
            n += 1
    return n


