# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# Project Name:        MakeHuman
# Product Home Page:   http://www.makehuman.org/
# Code Home Page:      http://code.google.com/p/makehuman/
# Authors:             Thomas Larsson
# Script copyright (C) MakeHuman Team 2001-2013
# Coding Standards:    See http://www.makehuman.org/node/165

"""
Abstract

Load a save poses
"""

import bpy
import os
import sys
import math
from mathutils import Vector, Quaternion, Matrix
from bpy.props import *
from bpy_extras.io_utils import ExportHelper, ImportHelper

from . import mh
from . import utils
from .utils import round

#----------------------------------------------------------
#   saveMhpFile(context, filepath):
#   loadMhpFile(context, filepath):
#----------------------------------------------------------

def saveMhpFile(context, filepath):
    ob = context.object
    rig = ob.parent
    scn = context.scene
    if rig and rig.type == 'ARMATURE':
        roots = rigRoots(rig)
        if len(roots) > 1:
            raise NameError("Armature %s has multiple roots: %s" % (rig.name, roots))
        (pname, ext) = os.path.splitext(filepath)
        mhppath = pname + ".mhp"

        fp = open(mhppath, "w", encoding="utf-8", newline="\n")
        root = rig.pose.bones[roots[0]]
        writeMhpBones(fp, root)
        fp.close()
        print(("Mhp file %s saved" % mhppath))


def writeMhpBones(fp, pb):
    b = pb.bone
    if pb.parent:
        string = "quat"
        mat = b.matrix_local.inverted() * b.parent.matrix_local * pb.parent.matrix.inverted() * pb.matrix
    else:
        string = "gquat"
        mat = pb.matrix.copy()
        maty = mat[1].copy()
        matz = mat[2].copy()
        mat[1] = matz
        mat[2] = -maty
    q = mat.to_quaternion()
    magn = math.sqrt(q.x*q.x + q.y*q.y + q.z*q.z)
    if magn > 1e-5:
        fp.write("%s\t%s\t%s\t%s\t%s\t%s\n" % (pb.name, string, round(q.w), round(q.x), round(q.y), round(q.z)))
    for child in pb.children:
        writeMhpBones(fp, child)


def loadMhpFile(context, filepath):
    ob = context.object
    rig = ob.parent
    scn = context.scene
    if rig and rig.type == 'ARMATURE':
        (pname, ext) = os.path.splitext(filepath)
        mhppath = pname + ".mhp"

        fp = open(mhppath, "rU")
        for line in fp:
            words = line.split()
            if len(words) < 5:
                continue
            elif words[1] == "quat":
                q = Quaternion((float(words[2]), float(words[3]), float(words[4]), float(words[5])))
                mat = q.to_matrix().to_4x4()
                pb = rig.pose.bones[words[0]]
                pb.matrix_basis = mat
            elif words[1] == "gquat":
                q = Quaternion((float(words[2]), float(words[3]), float(words[4]), float(words[5])))
                mat = q.to_matrix().to_4x4()
                maty = mat[1].copy()
                matz = mat[2].copy()
                mat[1] = -matz
                mat[2] = maty
                pb = rig.pose.bones[words[0]]
                pb.matrix_basis = pb.bone.matrix_local.inverted() * mat
        fp.close()
        print(("Mhp file %s loaded" % mhppath))



class VIEW3D_OT_LoadMhpButton(bpy.types.Operator):
    bl_idname = "mh.load_mhp"
    bl_label = "Load MHP File"
    bl_description = "Load a pose in MHP format"
    bl_options = {'UNDO'}

    filename_ext = ".mhp"
    filter_glob = StringProperty(default="*.mhp", options={'HIDDEN'})
    filepath = bpy.props.StringProperty(
        name="File Path",
        description="File path used for mhp file",
        maxlen= 1024, default= "")

    @classmethod
    def poll(self, context):
        return context.object

    def execute(self, context):
        loadMhpFile(context, self.properties.filepath)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class VIEW3D_OT_SaveasMhpFileButton(bpy.types.Operator, ExportHelper):
    bl_idname = "mh.saveas_mhp"
    bl_label = "Save MHP File"
    bl_description = "Save current pose in MHP format"
    bl_options = {'UNDO'}

    filename_ext = ".mhp"
    filter_glob = StringProperty(default="*.mhp", options={'HIDDEN'})
    filepath = bpy.props.StringProperty(
        name="File Path",
        description="File path used for mhp file",
        maxlen= 1024, default= "")

    @classmethod
    def poll(self, context):
        return context.object

    def execute(self, context):
        saveMhpFile(context, self.properties.filepath)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

#----------------------------------------------------------
#   saveBvhFile(context, filepath):
#   loadBvhFile(context, filepath):
#----------------------------------------------------------

import io_anim_bvh
from io_anim_bvh import export_bvh, import_bvh

def saveBvhFile(context, filepath):
    ob = context.object
    rig = ob.parent
    scn = context.scene
    if rig and rig.type == 'ARMATURE':
        roots = rigRoots(rig)
        if len(roots) > 1:
            raise NameError("Armature %s has multiple roots: %s" % (rig.name, roots))
        scn.objects.active = rig
        (pname, ext) = os.path.splitext(filepath)
        bvhpath = pname + ".bvh"

        export_bvh.write_armature(context, bvhpath,
           frame_start = scn.frame_current,
           frame_end = scn.frame_current,
           global_scale = 1.0,
           rotate_mode = scn.MhExportRotateMode,
           root_transform_only = True
           )
        scn.objects.active = ob
        print(("Saved %s" % bvhpath))
        return True
    else:
        return False


def rigRoots(rig):
    roots = []
    for bone in rig.data.bones:
        if not bone.parent:
            roots.append(bone.name)
    return roots


def loadBvhFile(context, filepath):
    ob = context.object
    rig = ob.parent
    scn = context.scene
    if rig and rig.type == 'ARMATURE':
        (pname, ext) = os.path.splitext(filepath)
        bvhpath = pname + ".bvh"

        bvh_nodes = import_bvh.read_bvh(context, bvhpath,
            rotate_mode=scn.MhImportRotateMode,
            global_scale=1.0)

        frame_orig = context.scene.frame_current

        bvh_name = bpy.path.display_name_from_filepath(bvhpath)

        import_bvh.bvh_node_dict2armature(context, bvh_name, bvh_nodes,
                               rotate_mode = scn.MhImportRotateMode,
                               frame_start = scn.frame_current,
                               IMPORT_LOOP = False,
                               global_matrix = rig.matrix_world,
                               )
        context.scene.frame_set(frame_orig)

        tmp = context.object
        bpy.ops.object.mode_set(mode='POSE')
        scn.objects.active = rig
        bpy.ops.object.mode_set(mode='POSE')
        copyPose(tmp, rig)
        scn.objects.active = ob
        scn.objects.unlink(tmp)
        del tmp
        print(("Loaded %s" % bvhpath))
        return True
    else:
        return False


def copyPose(src, trg):
    for name,srcBone in list(src.pose.bones.items()):
        trgBone = trg.pose.bones[srcBone.name]
        s = srcBone.matrix_basis
        t = trgBone.matrix_basis.copy()
        for i in range(3):
            for j in range(3):
                t[i][j] = s[i][j]
        trgBone.matrix_basis = t


class VIEW3D_OT_LoadBvhButton(bpy.types.Operator):
    bl_idname = "mh.load_bvh"
    bl_label = "Load BVH File"
    bl_description = "Load a pose in BVH format"
    bl_options = {'UNDO'}

    filename_ext = ".bvh"
    filter_glob = StringProperty(default="*.bvh", options={'HIDDEN'})
    filepath = bpy.props.StringProperty(
        name="File Path",
        description="File path used for bvh file",
        maxlen= 1024, default= "")

    @classmethod
    def poll(self, context):
        return context.object

    def execute(self, context):
        loadBvhFile(context, self.properties.filepath)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class VIEW3D_OT_SaveasBvhFileButton(bpy.types.Operator, ExportHelper):
    bl_idname = "mh.saveas_bvh"
    bl_label = "Save BVH File"
    bl_description = "Save current pose in BVH format"
    bl_options = {'UNDO'}

    filename_ext = ".bvh"
    filter_glob = StringProperty(default="*.bvh", options={'HIDDEN'})
    filepath = bpy.props.StringProperty(
        name="File Path",
        description="File path used for bvh file",
        maxlen= 1024, default= "")

    @classmethod
    def poll(self, context):
        return context.object

    def execute(self, context):
        saveBvhFile(context, self.properties.filepath)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

#----------------------------------------------------------
#   Convert weights
#----------------------------------------------------------

def readWeights(filepath, nVerts):
    weights = {}
    for n in range(nVerts):
        weights[n] = []
    bone = None
    fp = open(filepath, "rU")
    for line in fp:
        words = line.split()
        if len(words) < 2:
            pass
        elif words[0] == "#":
            if words[1] == "weights":
                bone = words[2]
            else:
                bone = None
        elif bone:
            vn = int(words[0])
            if vn < mh.NBodyVerts:
                weights[vn].append( (bone, float(words[1])) )
    fp.close()

    normedWeights = {}
    for vn,data in list(weights.items()):
        wsum = 0.0
        for bone,w in data:
            wsum += w
        ndata = []
        for bone,w in data:
            ndata.append((bone,w/wsum))
        normedWeights[vn] = ndata

    return normedWeights


def defineMatrices(rig):
    mats = {}
    for pb in rig.pose.bones:
        mats[pb.name] = pb.matrix * pb.bone.matrix_local.inverted()
    return mats


def getPoseLocs(mats, restLocs, weights, nVerts):
    locs = {}
    for n in range(nVerts):
        if weights[n]:
            mat = getMatrix(mats, weights[n])
            locs[n] = mat * restLocs[n]
        else:
            locs[n] = restLocs[n]
    return locs


def getRestLocs(mats, poseLocs, weights, nVerts):
    locs = {}
    for n in range(nVerts):
        if weights[n]:
            mat = getMatrix(mats, weights[n])
            locs[n] = mat.inverted() * poseLocs[n]
        else:
            locs[n] = poseLocs[n]
    return locs


def getMatrix(mats, weight):
    mat = Matrix()
    mat.zero()
    for bname,w in weight:
        mat += w * mats[bname]
    return mat


def getShapeLocs(ob, nVerts):
    locs = {}
    filename = "test"
    for n in range(nVerts):
        locs[n] = Vector((0,0,0))
    for skey in ob.data.shape_keys.key_blocks:
        if skey.name == "Basis":
            continue
        filename = skey.name
        for n,v in enumerate(skey.data):
            bv = ob.data.vertices[n]
            vec = v.co - bv.co
            locs[n] += skey.value*vec
    return locs, filename


def addLocs(locs1, locs2, nVerts):
    locs = {}
    for n in range(nVerts):
        locs[n] = locs1[n] + locs2[n]
    return locs


def subLocs(locs1, locs2, nVerts):
    locs = {}
    for n in range(nVerts):
        locs[n] = locs1[n] - locs2[n]
    return locs


def saveNewTarget(filepath, locs, nVerts):
    fp = open(filepath, "w", encoding="utf-8", newline="\n")
    locList = list(locs.items())
    locList.sort()
    for (n, dr) in locList:
        if dr.length > Epsilon:
            fp.write("%d %s %s %s\n" % (n, round(dr[0]), round(dr[2]), round(-dr[1])))
    fp.close()
    return


class VIEW3D_OT_ConvertRigButton(bpy.types.Operator):
    bl_idname = "mh.convert_rig"
    bl_label = "Convert to rig"
    bl_description = ""
    bl_options = {'UNDO'}

    @classmethod
    def poll(self, context):
        return context.object

    def execute(self, context):
        scn = context.scene
        ob = context.object
        rig = ob.parent
        nVerts = len(ob.data.vertices)
        oldWeights = readWeights(os.path.join(scn.MhProgramPath, "data/rigs", scn.MhSourceRig+".rig"), nVerts)
        newWeights = readWeights(os.path.join(scn.MhProgramPath, "data/rigs",scn.MhTargetRig+".rig"), nVerts)
        mats = defineMatrices(rig)
        restLocs = {}
        for n in range(nVerts):
            restLocs[n] = ob.data.vertices[n].co
        oldShapeDiffs, filename = getShapeLocs(ob, nVerts)
        oldRestLocs = addLocs(restLocs, oldShapeDiffs, nVerts)
        globalLocs = getPoseLocs(mats, oldRestLocs, oldWeights, nVerts)
        newRestLocs = getRestLocs(mats, globalLocs, newWeights, nVerts)
        newShapeDiffs = subLocs(newRestLocs, restLocs, nVerts)
        saveNewTarget(os.path.join(scn.MhProgramPath, "data/poses", scn.MhPoseTargetDir, filename + ".target"), newShapeDiffs, nVerts)

        return{'FINISHED'}

#----------------------------------------------------------
#   Init
#----------------------------------------------------------

def init():
    bpy.types.Scene.MhSourceRig = StringProperty(default = "rigid")
    bpy.types.Scene.MhTargetRig = StringProperty(default = "soft1")
    bpy.types.Scene.MhPoseTargetDir = StringProperty(default = "dance1-soft1")

    bpy.types.Scene.MhImportRotateMode = EnumProperty(
            name="Rotation",
            description="Rotation conversion",
            items=(('QUATERNION', "Quaternion",
                    "Convert rotations to quaternions"),
                   ('NATIVE', "Euler (Native)", ("Use the rotation order "
                                                 "defined in the BVH file")),
                   ('XYZ', "Euler (XYZ)", "Convert rotations to euler XYZ"),
                   ('XZY', "Euler (XZY)", "Convert rotations to euler XZY"),
                   ('YXZ', "Euler (YXZ)", "Convert rotations to euler YXZ"),
                   ('YZX', "Euler (YZX)", "Convert rotations to euler YZX"),
                   ('ZXY', "Euler (ZXY)", "Convert rotations to euler ZXY"),
                   ('ZYX', "Euler (ZYX)", "Convert rotations to euler ZYX"),
                   ),
            default='NATIVE',
            )

    bpy.types.Scene.MhExportRotateMode = EnumProperty(
            name="Rotation",
            description="Rotation conversion",
            items=(('NATIVE', "Euler (Native)",
                    "Use the rotation order defined in the BVH file"),
                   ('XYZ', "Euler (XYZ)", "Convert rotations to euler XYZ"),
                   ('XZY', "Euler (XZY)", "Convert rotations to euler XZY"),
                   ('YXZ', "Euler (YXZ)", "Convert rotations to euler YXZ"),
                   ('YZX', "Euler (YZX)", "Convert rotations to euler YZX"),
                   ('ZXY', "Euler (ZXY)", "Convert rotations to euler ZXY"),
                   ('ZYX', "Euler (ZYX)", "Convert rotations to euler ZYX"),
                   ),
            default='ZYX',
            )
