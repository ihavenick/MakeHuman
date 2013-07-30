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

Pose
"""

import log
import mh

import exportutils

from . import mhx_drivers

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------

def writePose(fp, env):
    amt = env.armature
    config = env.config

    fp.write("""
# --------------- Shapekeys ----------------------------- #
""")

    proxyShapes('Cage', 'T_Cage', env, fp)
    proxyShapes('Proxy', 'T_Proxy', env, fp)
    proxyShapes('Clothes', 'T_Clothes', env, fp)
    proxyShapes('Hair', 'T_Clothes', env, fp)
    proxyShapes('Eyes', 'T_Clothes', env, fp)

    fp.write("#if toggle&T_Mesh\n")
    writeShapeKeys(fp, env, "%sMesh" % env.name, None)

    fp.write("""
#endif

# --------------- Actions ----------------------------- #

#if toggle&T_Armature
""")

    fp.write(
        "Pose %s\n" % env.name +
        "end Pose\n")
    #amt.writeAllActions(fp)

    fp.write("Pose %s\n" % env.name)
    amt.writeControlPoses(fp, config)
    fp.write("  ik_solver 'LEGACY' ;\nend Pose\n")
    amt.writeDrivers(fp)
    fp.write("CorrectRig %s ;\n" % env.name)
    fp.write("""
#endif
""")


# *** material-drivers

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------

def proxyShapes(typ, test, env, fp):
    fp.write("#if toggle&%s\n" % test)
    for proxy in env.proxies.values():
        if proxy.name and proxy.type == typ:
            writeShapeKeys(fp, env, env.name+proxy.name+"Mesh", proxy)
    fp.write("#endif\n")


def writeCorrectives(fp, env, drivers, folder, landmarks, proxy, t0, t1):
    amt = env.armature
    empties = []
    try:
        shapeList = amt.loadedShapes[folder]
    except KeyError:
        shapeList = None
    if shapeList is None:
        shapeList = exportutils.shapekeys.readCorrectives(drivers, env.human, folder, landmarks, t0, t1)
        amt.loadedShapes[folder] = shapeList
    for (shape, pose, lr) in shapeList:
        empty = writeShape(fp, pose, lr, shape, 0, 1, proxy, env.config.scale)
        if empty:
            empties.append(pose)
    return empties


def writeShapeHeader(fp, pose, lr, min, max):
    fp.write(
        "ShapeKey %s %s True\n" % (pose, lr) +
        "  slider_min %.3g ;\n" % min +
        "  slider_max %.3g ;\n" % max)


def writeShape(fp, pose, lr, shape, min, max, proxy, scale):
    if proxy:
        pshapes = proxy.getShapes([("shape",shape)], scale)
        if len(pshapes) > 0:
            name,pshape = pshapes[0]
            if len(pshape.keys()) > 0:
                writeShapeHeader(fp, pose, lr, min, max)
                for (pv, dr) in pshape.items():
                    (dx, dy, dz) = dr
                    fp.write("  sv %d %.4f %.4f %.4f ;\n" %  (pv, dx, -dz, dy))
                fp.write("end ShapeKey\n")
                return False
    else:
        writeShapeHeader(fp, pose, lr, min, max)
        for (vn, dr) in shape.items():
           fp.write("  sv %d %.4f %.4f %.4f ;\n" %  (vn, scale*dr[0], -scale*dr[2], scale*dr[1]))
        fp.write("end ShapeKey\n")
        return False
    return True


def writeShapeKeys(fp, env, name, proxy):
    amt = env.armature
    config = env.config
    scale = config.scale

    isHuman = ((not proxy) or proxy.type == 'Proxy')
    isHair = (proxy and proxy.type in ['Hair','Eyes'])
    useCorrectives = (
        False and
        config.bodyShapes and
        amt.options.rigtype == "mhx" and
        ((not proxy) or (proxy.type in ['Proxy', 'Clothes']))
    )

    fp.write(
"#if toggle&T_Shapekeys\n" +
"ShapeKeys %s\n" % name +
"  ShapeKey Basis Sym True\n" +
"  end ShapeKey\n")

    if isHuman and amt.options.facepanel:
        shapeList = exportutils.shapekeys.readFaceShapes(env.human, rig_panel.BodyLanguageShapeDrivers, 0.6, 0.7)
        for (pose, shape, lr, min, max) in shapeList:
            writeShape(fp, pose, lr, shape, min, max, proxy, scale)

    if isHuman and config.expressions:
        try:
            shapeList = env.loadedShapes["expressions"]
        except KeyError:
            shapeList = None
        if shapeList is None:
            shapeList = exportutils.shapekeys.readExpressionUnits(env.human, 0.7, 0.9)
            env.loadedShapes["expressions"] = shapeList
        for (pose, shape) in shapeList:
            writeShape(fp, pose, "Sym", shape, -1, 2, proxy, scale)

    if useCorrectives:
        shoulder = writeCorrectives(fp, env, rig_mhx.ShoulderTargetDrivers, "shoulder", "shoulder", proxy, 0.88, 0.90)
        hips = writeCorrectives(fp, env, rig_mhx.HipTargetDrivers, "hips", "hips", proxy, 0.90, 0.92)
        elbow = writeCorrectives(fp, env, rig_mhx.ElbowTargetDrivers, "elbow", "body", proxy, 0.92, 0.94)
        knee = writeCorrectives(fp, env, rig_mhx.KneeTargetDrivers, "knee", "knee", proxy, 0.94, 0.96)

    if isHuman:
        for path,name in env.customTargetFiles:
            try:
                shape = env.loadedShapes[path]
            except KeyError:
                shape = None
            if shape is None:
                log.message("    %s", path)
                shape = exportutils.custom.readCustomTarget(path)
                env.loadedShapes[path] = shape
            writeShape(fp, name, "Sym", shape, -1, 2, proxy, scale)

    fp.write("  AnimationData None (toggle&T_Symm==0)\n")

    if useCorrectives:
        mhx_drivers.writeTargetDrivers(fp, rig_mhx.ShoulderTargetDrivers, env.name, shoulder)
        mhx_drivers.writeTargetDrivers(fp, rig_mhx.HipTargetDrivers, env.name, hips)
        mhx_drivers.writeTargetDrivers(fp, rig_mhx.ElbowTargetDrivers, env.name, elbow)
        mhx_drivers.writeTargetDrivers(fp, rig_mhx.KneeTargetDrivers, env.name, knee)

        mhx_drivers.writeRotDiffDrivers(fp, rig_mhx.ArmShapeDrivers, proxy)
        mhx_drivers.writeRotDiffDrivers(fp, rig_mhx.LegShapeDrivers, proxy)
        #mhx_drivers.writeShapePropDrivers(fp, amt, rig_mhx.bodyShapes, proxy, "Mha")

    fp.write("#if toggle&T_ShapeDrivers\n")

    if isHuman:
        for path,name in env.customTargetFiles:
            mhx_drivers.writeShapePropDrivers(fp, amt, [name], proxy, "Mhc")

        if config.expressions:
            mhx_drivers.writeShapePropDrivers(fp, amt, exportutils.shapekeys.ExpressionUnits, proxy, "Mhs")

        if amt.options.facepanel and amt.options.rigtype=='mhx':
            mhx_drivers.writeShapeDrivers(fp, amt, rig_panel.BodyLanguageShapeDrivers, proxy)

        skeys = []
        for (skey, val, string, min, max) in  env.customProps:
            skeys.append(skey)
        mhx_drivers.writeShapePropDrivers(fp, amt, skeys, proxy, "Mha")
    fp.write("#endif\n")

    fp.write("  end AnimationData\n\n")

    if config.expressions and not proxy:
        exprList = exportutils.shapekeys.readExpressionMhm(mh.getSysDataPath("expressions"))
        writeExpressions(fp, exprList, "Expression")
        visemeList = exportutils.shapekeys.readExpressionMhm(mh.getSysDataPath("visemes"))
        writeExpressions(fp, visemeList, "Viseme")

    fp.write(
        "  end ShapeKeys\n" +
        "#endif\n")
    return


def writeExpressions(fp, exprList, label):
    for (name, units) in exprList:
        fp.write("  %s %s\n" % (label, name))
        for (unit, value) in units:
            fp.write("    %s %s ;\n" % (unit, value))
        fp.write("  end\n")

